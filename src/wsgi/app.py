from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def login():
	if request.method == 'POST':
		session['logged_in'] = True
		return redirect(url_for('report_filter'))
    return render_template('login.html')

@app.route('/report_filter', methods=['GET', 'POST'])
def report_filter():
	if request.method == 'POST':
		if request.form['filter'] == 'Facility':
			return redirect(url_for('facility_report'))
		elif request.form['filter'] == 'Transit':
			return redirect(url_for('transit_report'))
	return render_template('report_filter.html')

@app.route('/facility_report')
def facility_report():
	#For now, just return the page
	return render_template('facility_report.html')

@app.route('/transit_report')
def transit_report():
	#For now, just return the page
	return render_template('transit_report.html')

@app.route('/logout')
def logout():
	#For now, just return the page
	return render_template('logout.html')