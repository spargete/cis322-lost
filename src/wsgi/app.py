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
	cur.execute("SELECT facilities.common_name, assets.asset_tag, assets.description, asset_at.arrive_dt, asset_at.depart_dt FROM \
	facilities inner join asset_at on facilities.facility_pk=asset_at.facility_fk inner join assets on asset_at.asset_fk=assets.asset_pk \
	where facilities.fcode=%s and asset_at.arrive_dt<=%s and asset_at.depart_dt>=%s;",(session["filter_fcode"],session["filter_date"],session["filter_date"]))
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
	#For now, just return the page
	return render_template('transit_report.html')

@app.route('/logout')
def logout():
	session['logged_in'] = False
	return render_template('logout.html')