# login.py
from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import bcrypt

app = Flask(__name__)
app.secret_key = 'your_secret_key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = False

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM user WHERE username = ?', (username,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(password, user['password']):
            session['loggedin'] = True
            session['username'] = username

            if username == 'Admin':
                session['admin_login'] = True
                return redirect('/admin')
            else:
                return redirect('/stream')
        else:
            error = True
            flash('Incorrect Username or Password', 'danger')

    return render_template('login.html', error=error)

@app.route('/admin')
def admin_panel():
    if session.get('admin_login'):
        return "<h1>Welcome Admin</h1>"
    return redirect('/login')

@app.route('/stream')
def stream_page():
    if session.get('loggedin'):
        return "<h1>Welcome to Stream Page</h1>"
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
