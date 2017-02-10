from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
from config import dbname, dbhost, dbport, secret_key, lost_pub
import json


app = Flask(__name__)

app.config["SECRET_KEY"] = secret_key

@app.route('/', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['logged_in'] = True
		return redirect(url_for('report_filter'))
	return render_template('login.html')

@app.route('/report_filter', methods=['GET', 'POST'])
def report_filter():
	if request.method == 'POST':
		session["filter_date"] = request.form["filter_date"]
		session["filter_fcode"] = request.form["filter_fcode"]
		if request.form['filter'] == 'Facility':
			return redirect(url_for('facility_report'))
		elif request.form['filter'] == 'Transit':
			return redirect(url_for('transit_report'))
	return render_template('report_filter.html')

@app.route('/facility_report')
def facility_report():
	conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
	cur = conn.cursor()
	cur.execute("SELECT facilities.common_name, assets.asset_tag, assets.description, asset_at.arrive_dt, asset_at.depart_dt FROM \
	facilities INNER JOIN asset_at ON facilities.facility_pk=asset_at.facility_fk INNER JOIN assets ON asset_at.asset_fk=assets.asset_pk \
	WHERE facilities.fcode=%s AND asset_at.arrive_dt<=%s AND asset_at.depart_dt>=%s;",(session["filter_fcode"],session["filter_date"],session["filter_date"]))
	result = cur.fetchall()
	facility_report = []
	for r in result:
		row = dict()
		row["common_name"] = r[0]
		row["asset_tag"] = r[1]
		row["asset_description"] = r[2]
		row["arrive_dt"] = r[3]
		row["depart_dt"] = r[4]
		facility_report.append(row)

	session["facility_report"] = facility_report
	return render_template('facility_report.html')

@app.route('/transit_report')
def transit_report():
	conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
	cur = conn.cursor()
	cur.execute("SELECT facilities.common_name, assets.asset_tag, assets.description, asset_on.load_dt, asset_on.unload_dt, convoys.request \
	FROM asset_on \
	INNER JOIN convoys ON asset_on.convoy_fk=convoys.convoy_pk \
	INNER JOIN assets ON asset_on.asset_fk=assets.asset_pk \
	INNER JOIN facilities ON convoys.source_fk=facilities.facility_pk \
	WHERE asset_on.load_dt<=%s \
	AND asset_on.unload_dt>=%s;",(session["filter_date"],session["filter_date"]))
	result = cur.fetchall()
	transit_report = []
	for r in result:
		row = dict()
		cur.execute("SELECT facilities.common_name FROM facilities INNER JOIN convoys ON convoys.dest_fk=facilities.facility_pk WHERE convoys.request=%s;", (r[5],))
		dest = cur.fetchone()
		row["source"] = r[0]
		row["destination"] = dest[0]
		row["asset_tag"] = r[1]
		row["asset_description"] = r[2]
		row["load_dt"] = r[3]
		row["unload_dt"] = r[4]
		transit_report.append(row)

	session["transit_report"] = transit_report
	return render_template('transit_report.html')

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return render_template('logout.html')

@app.route('/rest')
def rest():
	return render_template('rest.html')

@app.route('/rest/lost_key')
def lost_key():
	if request.method = "POST" and "arguments" in request.form:	
		req = json.loads(request.form["arguments"])
		dat = dict()
		dat["timestamp"] = req["timestamp"]

		with open(lost_key) as f:
			key = f.read()
			if key == '':
				dat["result"] = "FAIL"
			else:
				dat["result"] = "OK"
			dat["key"] = key

		data = json.dumps(dat)
		return data

@app.route('/rest/activate_user', methods=("POST",))
def activate_user():
	if request.method = "POST" and "arguments" in request.form:
		req = json.loads(request.form["arguments"])
		dat = dict()
		dat["timestamp"] = req["timestamp"]
		#SQL query stuff to do the thing >_>
		conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
		cur = conn.cursor()
		cur.execute("SELECT user_pk, active FROM users WHERE username=%s;", (req["username"],))
		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result == None:
			dat["result"] = "NEW"
			cur.execute("INSERT INTO users (username, active) VALUES (%s, TRUE)", (req["username"],))
		elif result[1] == False:
			dat["result"] = "OK"
			cur.execute("UPDATE users SET active=TRUE WHERE username=%s", (req["username"],))
		else:
			dat["result"] = "FAIL"

		data = json.dumps(dat)
		return data

@app.route('/rest/suspend_user')
def suspend_user():
	if request.method = "POST" and "arguments" in request.form:
		req = json.loads(request.form["arguments"])
		dat = dict()
		dat["timestamp"] = req["timestamp"]
		dat["result"] = "OK"

		conn = psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
		cur = conn.cursor()
		cur.execute("SELECT user_pk, active FROM users WHERE username=%s", (req["username"],))

		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = False

		if result != False:
			cur.execute("UPDATE users SET active=FALSE WHERE username=%s", (req["username"],))

		data = json.dumps(dat)
		return data

@app.route('/rest/list_products')
def list_products():
	if request.method = "POST" and "arguments" in request.form:
		req = json.loads(request.form["arguments"])
		dat = dict()
		dat["timestamp"] = req["timestamp"]
		##Told to steal code directly from Dan's implementation, so that's exactly what I'm going to do
		dat["result"] = "OK"
		data = json.dumps(dat)
		return data

@app.route('/rest/add_products')
def add_products():
	if request.method = "POST" and "arguments" in request.form:
		req = json.loads(request.form["arguments"])
		dat = dict()
		dat["timestamp"] = req["timestamp"]
		##TODO
		dat["result"] = "OK"
		data = json.dumps(dat)
		return data

@app.route('/rest/add_asset')
def add_asset():
	if request.method = "POST" and "arguments" in request.form:
		req = json.loads(request.form["arguments"])
		dat = dict()
		dat["timestamp"] = req["timestamp"]
		##TODO
		dat["result"] = "OK"
		data = json.dumps(dat)
		return data