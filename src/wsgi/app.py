from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
from config import dbname, dbhost, dbport, secret_key

app = Flask(__name__)

app.config["SECRET_KEY"] = secret_key

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return redirect(url_for('login'))

@app.route('/create_user', methods = ['GET', 'POST'])
def create_user():
	if request.method == 'POST':
		conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
		cur = conn.cursor()
		username = request.form['username']
		password = request.form['password']
		role = request.form['role']
		cur.execute('SELECT username FROM users WHERE username=%s;', (username,))
		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result == None:
			cur.execute('INSERT INTO users (username, password) VALUES (%s, %s);', (username, password))
			cur.execute('INSERT INTO user_is (role_fk, user_fk) VALUES ((SELECT role_pk FROM roles WHERE role_name=%s), (SELECT user_pk FROM users WHERE username=%s));', (role, username))
			conn.commit()
			cur.close()
			conn.close()
			return render_template('user_added.html')
		else:
			cur.close()
			conn.close()
			return render_template('user_exists.html')

	return render_template('create_user.html')

@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
		cur = conn.cursor()
		username = request.form['username']
		password = request.form['password']
		cur.execute('SELECT username, password, role_name FROM users INNER JOIN user_is ON user_pk=user_fk INNER JOIN roles ON role_pk=role_fk WHERE username=%s AND password=%s;', (username, password))
		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result == None:
			cur.close()
			conn.close()
			return render_template('incorrect_credentials.html')
		else:
			cur.close()
			conn.close()
			session['username'] = username
			session['logged_in'] = True
			session['role'] = result[2]
			return redirect(url_for('dashboard'))

	return render_template('login.html')

@app.route('/dashboard', methods = ['GET',])
def dashboard():
	if not session['logged_in']:
		return redirect(url_for('login'))
	else:
		#Add SQL query to grab correct details for the form for Step 3
		return render_template('dashboard.html')


@app.route('/add_facility', methods = ['GET', 'POST'])
def add_facility():
	if not session['logged_in']:
		return redirect(url_for('login'))

	conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
	cur = conn.cursor()
	cur.execute('SELECT facility_common_name, facility_fcode FROM facilities;')

	try:
		result = cur.fetchall()
	except ProgrammingError:
		result = None

	facility_report = []
	for r in result:
		row = dict()
		row['common_name'] = r[0]
		row['fcode'] = r[1]
		facility_report.append(row)

	session['facility_report'] = facility_report
	if request.method == 'POST':
		fcode = request.form['fcode']
		common_name = request.form['common_name']

		cur.execute('SELECT facility_fcode, facility_common_name FROM facilities WHERE facility_fcode=%s OR facility_common_name=%s;', (fcode, common_name))

		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result == None:
			cur.execute('INSERT INTO facilities (facility_fcode, facility_common_name) VALUES (%s, %s);', (fcode, common_name))
			conn.commit()
			cur.close()
			conn.close()
			return redirect(url_for('add_facility'))
		else:
			cur.close()
			conn.close()
			return render_template('facility_exists.html')

	cur.close()
	conn.close()
	return render_template('add_facility.html')

@app.route('/add_asset', methods = ['GET', 'POST'])
def add_asset():
	if not session['logged_in']:
		return redirect(url_for('login'))

	conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
	cur = conn.cursor()
	cur.execute('SELECT a.asset_tag, a.description, aa.arrive_dt, aa.depart_dt, \
		f.facility_common_name, f.facility_fcode FROM assets AS a INNER JOIN \
		asset_at AS aa ON aa.asset_fk=a.asset_pk INNER JOIN facilities AS f \
		ON f.facility_pk=aa.facility_fk ORDER BY aa.arrive_dt ASC;')

	try:
		result = cur.fetchall()
	except ProgrammingError:
		result = None

	asset_report = []
	for r in result:
		row = dict()
		row['asset_tag'] = r[0]
		row['description'] = r[1]
		row['arrive_dt'] = r[2]
		row['depart_dt'] = r[3]
		row['facility_name'] = r[4]
		row['facility_fcode'] = r[5]
		asset_report.append(row)

	session['asset_list'] = asset_report

	cur.execute('SELECT facility_common_name FROM facilities;')
	try:
		result = cur.fetchall()
	except ProgrammingError:
		result = None

	facility_list = []
	for r in result:
		row = dict()
		row['facility_name'] = r[0]
		facility_list.append(row)

	session['facility_list'] = facility_list

	if request.method == 'POST':
		asset_tag = request.form['asset_tag']
		description = request.form['description']
		name = request.form['facility_name']
		arrive_dt = request.form['arrive_dt']

		cur.execute('SELECT asset_tag FROM assets WHERE asset_tag=%s', (asset_tag,))

		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result == None:
			cur.execute('INSERT INTO assets (asset_tag, description) VALUES (%s, %s);', (asset_tag, description))
			cur.execute('INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES ((SELECT asset_pk FROM assets WHERE asset_tag=%s), \
				(SELECT facility_pk FROM facilities WHERE facility_common_name=%s), %s);', (asset_tag, name, arrive_dt))
			conn.commit()
			cur.close()
			conn.close()
			return redirect(url_for('add_asset'))
		else:
			cur.close()
			conn.close()
			return render_template('asset_exists.html')

	cur.close()
	conn.close()
	return render_template('add_asset.html')

@app.route('/dispose_asset', methods = ['GET', 'POST'])
def dispose_asset():
	if not session['logged_in']:
		return redirect(url_for('login'))

	if session['role'] != 'Logistics Officer':
		return render_template('disposal_locked.html')
	if request.method == 'POST':
		tag = request.form['asset_tag']
		date = request.form['disposal_date']
		conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
		cur = conn.cursor()
		cur.execute('SELECT disposed_dt FROM assets WHERE asset_tag=%s;', (tag,))

		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result == None:
			cur.close()
			conn.close()
			return render_template('no_matching_asset.html')
		elif result[0] != None:
			session['disposed_dt'] = result[0]
			cur.close()
			conn.close()
			return render_template('asset_already_disposed.html')
		else:
			cur.execute('UPDATE assets SET disposed_dt=%s WHERE asset_tag=%s;', (date, tag))
			cur.execute('UPDATE asset_at SET depart_dt=%s WHERE depart_dt IS NULL FROM asset_at WHERE asset_fk=(SELECT asset_pk FROM assets WHERE asset_tag=%s)) \
				AND asset_fk=(SELECT asset_pk FROM assets WHERE asset_tag=%s);', (date, tag, tag))
			conn.commit()
			cur.close()
			conn.close()
			return redirect(url_for('dashboard'))

	return render_template('dispose_asset.html')

@app.route('/asset_report', methods = ['GET', 'POST'])
def asset_report():
	if not session['logged_in']:
		return redirect(url_for('login'))
	
	session['asset_report'] = []
	if request.method == 'POST':
		facility = request.form['facility']
		date = request.form['date']
		conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
		cur = conn.cursor()
		if facility == 'All':
			cur.execute('SELECT a.asset_tag, a.description, f.facility_common_name, aa.arrive_dt, aa.depart_dt FROM assets AS a INNER JOIN asset_at AS aa ON a.asset_pk=aa.asset_fk \
			INNER JOIN facilities AS f ON f.facility_pk=aa.facility_fk WHERE aa.arrive_dt<=%s AND (aa.depart_dt>=%s OR aa.depart_dt IS NULL);', (date, date))
		else:
			cur.execute('SELECT a.asset_tag, a.description, f.facility_common_name, aa.arrive_dt, aa.depart_dt FROM assets AS a INNER JOIN asset_at AS aa ON a.asset_pk=aa.asset_fk \
			INNER JOIN facilities AS f ON f.facility_pk=aa.facility_fk WHERE aa.arrive_dt<=%s AND (aa.depart_dt>=%s OR aa.depart_dt IS NULL) AND f.facility_common_name=%s;', (date, date, facility))

		try:
			result = cur.fetchall()
		except ProgrammingError:
			result = None

		asset_report = []	

		for r in result:
			row = dict()
			row['asset_tag'] = r[0]
			row['description'] = r[1]
			row['facility'] = r[2]
			row['arrive_dt'] = r[3]
			row['depart_dt'] = r[4]
			asset_report.append(row)

		session['asset_report'] = asset_report

		cur.execute('SELECT facility_common_name FROM facilities;')
		try:
			result = cur.fetchall()
		except ProgrammingError:
			result = None

		facility_list = []
		for r in result:
			row = dict()
			row['facility_name'] = r[0]
			facility_list.append(row)

		session['facility_list'] = facility_list

	return render_template('asset_report.html')