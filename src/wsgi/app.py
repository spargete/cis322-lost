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
		cur.execute('SELECT username FROM users WHERE username=%s', (username,))
		try:
			result = cur.fetchone()
		except ProgrammingError:
			result = None

		if result == None:
			cur.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
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
		conn.psycopg2.connect(dbname=dbname, host=dbhost, port=dbport)
		cur = conn.cursor()
		username = request.form['username']
		password = request.form['password']
		cur.execute('SELECT username, password FROM users WHERE username=%s AND password=%s', (username, password))
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