from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
from config import dbname, dbhost, dbport, secret_key
from datetime import datetime

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
		conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
		cur = conn.cursor()		
		if session['role'] == 'Logistics Officer':
			cur.execute('SELECT request_fk, load_dt, unload_dt FROM transfers WHERE load_dt IS NULL OR unload_dt IS NULL;')
			try:
				request = cur.fetchall()
			except ProgrammingError:
				request = None


			todo = []
			for r in request:
				row = dict()
				row['req_id'] = r[0]
				row['load_dt'] = r[1]
				row['unload_dt'] = r[2]
				todo.append(row)

			session['todo'] = todo

		elif session['role'] == 'Facilities Officer':
			cur.execute('SELECT tr.request_pk, u.username, tr.request_dt FROM transfer_requests AS tr INNER JOIN \
				users AS u ON tr.requester_fk=u.user_pk WHERE approval_dt IS NULL;')
			try:
				request = cur.fetchall()
			except ProgrammingError:
				request = None

			todo = []
			for r in request:
				row = dict()
				row['req_id'] = r[0]
				row['requester'] = r[1]
				row['req_time'] = r[2]
				todo.append(row)

			session['todo'] = todo

		conn.commit()
		cur.close()
		conn.close()	
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

@app.route('/transfer_req', methods = ['GET', 'POST'])
def transfer_req():
	if not session['logged_in']:
		return redirect(url_for('login'))

	if session['role'] != 'Logistics Officer':
		return render_template('transfer_req_locked.html')

	conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
	cur = conn.cursor()

	if request.method == 'POST':
		tag = request.form['asset_tag']
		source = request.form['source_fcode']
		dest = request.form['dest_fcode']
		request_dt = str(datetime.now())

		cur.execute('SELECT asset_pk FROM assets WHERE asset_tag=%s;', (tag,))

		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result != None:
			asset_fk = result[0]
		else:
			conn.commit()
			cur.close()
			conn.close()
			return render_template('asset_tag_missing.html')

		cur.execute('SELECT facility_pk FROM facilities WHERE facility_fcode=%s;', (source,))

		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result != None:
			source_fk = result[0]
		else:
			conn.commit()
			cur.close()
			conn.close()
			return render_template('source_facility_missing.html')

		cur.execute('SELECT facility_pk FROM facilities WHERE facility_fcode=%s;', (dest,))

		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result != None:
			dest_fk = result[0]
		else:
			conn.commit()
			cur.close()
			conn.close()
			return render_template('dest_facility_missing.html')

		cur.execute('SELECT user_pk FROM users WHERE username=%s;', (session['username'],))

		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result != None:
			requester_fk = result[0]
		else:
			conn.commit()
			cur.close()
			conn.close()
			return render_template('generic_error.html')

		cur.execute('SELECT f.facility_fcode FROM assets AS a INNER JOIN asset_at AS aa ON a.asset_pk=aa.asset_fk INNER JOIN \
			facilities AS f ON f.facility_pk=aa.facility_fk WHERE aa.arrive_dt<=%s AND (aa.depart_dt>%s OR aa.depart_dt IS NULL) AND a.asset_tag=%s;', (request_dt, request_dt, tag))

		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result != None:
			if source != result[0]:
				conn.commit()
				cur.close()
				conn.close()
				return render_template('asset_not_at_source.html')
			elif dest == result[0]:
				conn.commit()
				cur.close()
				conn.close()
				return render_template('asset_already_at_dest.html')
		else:
			return render_template('generic_error.html')

		cur.execute('INSERT INTO transfer_requests (requester_fk, request_dt, source_fk, dest_fk, asset_fk) VALUES (%s, %s, %s, %s, %s);', (requester_fk, request_dt, source_fk, dest_fk, asset_fk))
		conn.commit()
		cur.close()
		conn.close()
		return render_template("request_successful.html")

	else:
		asset_list = []
		facility_list = []

		cur.execute('SELECT asset_tag FROM assets;')
		try:
			result = cur.fetchall()
		except ProgrammingError:
			result = None

		for r in result:
			row = dict()
			row['tag'] = r[0]
			asset_list.append(row)

		session['asset_list'] = asset_list

		cur.execute('SELECT facility_fcode FROM facilities;')
		try:
			result = cur.fetchall()
		except ProgrammingError:
			result = None

		for r in result:
			row = dict()
			row['fcode'] = r[0]
			facility_list.append(row)

		session['facility_list'] = facility_list

		conn.commit()
		cur.close()
		conn.close()

		return render_template('transfer_request.html')

@app.route('/approve_req', methods = ['GET', 'POST'])
def approve_req():
	if not session['logged_in']:
		return redirect(url_for('login'))

	if session['role'] != 'Facilities Officer':
		return render_template('approve_req_locked.html')

	conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
	cur = conn.cursor()

	if request.method == 'GET' and 'req_id' in request.args:
		req_id = int(request.args['req_id'])
		cur.execute('SELECT a.asset_tag, f.facility_common_name, u.username, r.request_dt FROM transfer_requests AS r INNER JOIN \
			facilities AS f ON r.source_fk=f.facility_pk INNER JOIN users AS u ON r.requester_fk=u.user_pk INNER JOIN assets AS a ON \
			r.asset_fk=a.asset_pk WHERE r.request_pk=%s;', (req_id,))

		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		cur.execute('SELECT f.facility_common_name FROM transfer_requests AS r INNER JOIN \
			facilities AS f ON r.dest_fk=f.facility_pk WHERE r.request_pk=%s;', (req_id,))

		try:
			result_dest = cur.fetchone()
		except ProgrammingError:
			result_dest = None

		if result == None or result_dest == None:
			conn.commit()
			cur.close()
			conn.close()
			return render_template('generic_error.html')
		else:
			session['request_report'] = []
			row = dict()
			row['tag'] = result[0]
			row['source'] = result[1]
			row['dest'] = result_dest[0]
			row['requester'] = result[2]
			row['request_dt'] = result[3]
			session['request_report'].append(row)

		conn.commit()
		cur.close()
		conn.close()
		return render_template('approve_req.html')

	elif request.method == 'POST':
		req_id = int(request.form['req_id'])
		approval = request.form['approval']
		if approval == 'False':
			cur.execute('DELETE FROM transfer_requests WHERE request_pk=%s;', (req_id,))
			conn.commit()
			cur.close()
			conn.close()
			return redirect(url_for('dashboard'))

		else:
			user = session['username']
			approval_dt = str(datetime.now())
			cur.execute('UPDATE transfer_requests SET approval_dt=%s, approver_fk=(SELECT user_pk FROM users WHERE username=%s) WHERE request_pk=%s;', (approval_dt, user, req_id))
			cur.execute('INSERT INTO transfers (asset_fk, request_fk) VALUES ((SELECT asset_fk FROM transfer_requests WHERE request_pk=%s), %s);', (req_id, req_id))
			conn.commit()
			cur.close()
			conn.close()
			return redirect(url_for('dashboard'))

	return render_template('generic_error.html')

@app.route('/update_transit', methods=['GET', 'POST'])
def update_transit():
	if not session['logged_in']:
		return redirect(url_for('login'))

	if session['role'] != 'Logistics Officer':
		return render_template('update_transit_locked.html')

	conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
	cur = conn.cursor()

	if request.method == 'GET' and 'transfer_id' in request.args:
		transfer_id = int(request.args['transfer_id'])
		cur.execute('SELECT t.load_dt, t.unload_dt, tr.source_fk, tr.dest_fk FROM transfers AS t INNER JOIN transfer_requests AS tr ON t.request_fk=tr.request_pk \
			WHERE t.request_fk=%s;', (transfer_id,))

		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result == None or result[1] != None:
			conn.commit()
			cur.close()
			conn.close()
			return render_template('transfer_invalid.html')

		conn.commit()
		cur.close()
		conn.close()
		return render_template('update_transit.html')

	elif request.method == 'POST':
		date = request.form['date']
		which = request.form['which']
		transfer_id = request.form['transfer_id']
		if which == 'load':
			#Check to see if asset is being moved after it arrives
			cur.execute('SELECT arrive_dt FROM asset_at WHERE depart_dt IS NULL AND asset_fk=(SELECT asset_fk FROM transfers WHERE request_fk=%s);', (transfer_id,))
			try:
				result = cur.fetchone()
			except ProgrammingError:
				conn.commit()
				cur.close()
				conn.close()
				return render_template('generic_error.html')

			if result == None or result[0] > datetime.strptime(date, '%Y-%m-%d'):
				conn.commit()
				cur.close()
				conn.close()
				return render_template('generic_error.html')

			#Check to see if a load_dt has already been set
			cur.execute('SELECT load_dt FROM transfers WHERE request_fk=%s;', (transfer_id,))
			try:
				result = cur.fetchone()
			except ProgrammingError:
				conn.commit()
				cur.close()
				conn.close()
				return render_template('transfer_invalid.html')

			if result[0] != None:
				conn.commit()
				cur.close()
				conn.close()
				return render_template('load_date_set.html')

			cur.execute('UPDATE transfers SET load_dt=%s WHERE request_fk=%s;', (date, transfer_id))
			cur.execute('UPDATE asset_at SET depart_dt=%s WHERE depart_dt IS NULL AND asset_fk=(SELECT asset_fk FROM transfers WHERE request_fk=%s);', (date, transfer_id))
			conn.commit()
			cur.close()
			conn.close()
			return redirect(url_for('dashboard'))
		elif which == 'unload':
			cur.execute('SELECT load_dt FROM transfers WHERE request_fk=%s;', (transfer_id))
			try:
				result = cur.fetchone()
			except ProgrammingError:
				cur.close()
				conn.close()
				return render_template('generic_error.html')

			if result[0] == None or date < result[0]:
				cur.close()
				conn.close()
				return render_template('load_date_incorrect.html')
			else:
				cur.execute('UPDATE transfers SET unload_dt=%s WHERE request_fk=%s;' (date, transfer_id))
				cur.execute('INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES \
					((SELECT asset_fk FROM transfers WHERE request_fk=%s), (SELECT dest_fk FROM transfer_requests WHERE request_pk=%s), %s);' (transfer_id, transfer_id, date))
				conn.commit()
				cur.close()
				conn.close()
				return redirect(url_for('dashboard'))

	return render_template('generic_error.html')
