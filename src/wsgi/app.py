from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
from config import dbname, dbhost, dbport, secret_key

app = Flask(__name__)

app.config["SECRET_KEY"] = secret_key

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
		cur.execute('SELECT username, password FROM users WHERE username=%s AND password=%s;', (username, password))
		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result == None:
			return render_template('incorrect_credentials.html')
		else:
			session['username'] = username
			session['logged_in'] = True
			return redirect(url_for('dashboard'))

	return render_template('login.html')

@app.route('/dashboard', methods = ['GET',])
def dashboard():
	return render_template('dashboard.html')


@app.route('/add_facility', methods = ['GET', 'POST'])
def add_facility():
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
			return redirect(url_for('add_facility'))
		else:
			return render_template('facility_exists.html')


	return render_template('add_facility.html')