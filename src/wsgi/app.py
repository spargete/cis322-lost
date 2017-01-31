from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report_filter')
def report_filter():
	return render_template('report_filter.html')