from flask import Flask, render_template, request, session, redirect, url_for
import psycopg2
from config import dbname, dbhost, dbport, secret_key

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
	cur.execute("SELECT * FROM facilities WHERE fcode=%s",(session["filter_fcode"],))
	result = cur.fetchall()
	facility_report = []
	for r in result:
		row = dict()
		row["fcode"] = r[1]
		row["common_name"] = r[2]
		facility_report.append(row)

	session["facility_report"] = facility_report
	return render_template('facility_report.html')

@app.route('/transit_report')
def transit_report():
	#For now, just return the page
	return render_template('transit_report.html')

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return render_template('logout.html')