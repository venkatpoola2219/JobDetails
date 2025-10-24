from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)
app.secret_key = "your_secret_key"

DB_FILE = "employees.db"

# -------- DATABASE ----------
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    designation TEXT,
                    salary INTEGER,
                    gender TEXT,
                    address TEXT,
                    company TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# -------- ROUTES ----------
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'venkat' and password == 'sukanyavenkat@1212':
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return render_template("admin_login.html", error="Invalid credentials")
    return render_template("admin_login.html")

@app.route('/admin')
def admin_dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('admin_login'))
    return render_template("admin.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

# -------- EMPLOYEE DATA ----------
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT INTO employees (name, designation, salary, gender, address, company)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (data['name'], data['designation'], data['salary'],
               data['gender'], data['address'], data['company']))
    conn.commit()
    conn.close()
    return jsonify({"message": "Employee saved successfully!"})

@app.route('/search')
def search():
    if not session.get('logged_in'):
        return jsonify({"status": "unauthorized"}), 401
    field = request.args.get('field')
    value = request.args.get('value')

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = f"SELECT * FROM employees WHERE LOWER({field}) LIKE ?"
    c.execute(query, ('%' + value.lower() + '%',))
    results = c.fetchall()
    conn.close()

    if not results:
        return jsonify({"status": "not_found"})

    employees = [
        {"id": r[0], "name": r[1], "designation": r[2],
         "salary": r[3], "gender": r[4], "address": r[5], "company": r[6]}
        for r in results
    ]
    return jsonify({"status": "ok", "results": employees})

@app.route('/all')
def all_employees():
    if not session.get('logged_in'):
        return jsonify({"status": "unauthorized"}), 401
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT * FROM employees")
    results = c.fetchall()
    conn.close()

    if not results:
        return jsonify({"status": "not_found"})

    employees = [
        {"id": r[0], "name": r[1], "designation": r[2],
         "salary": r[3], "gender": r[4], "address": r[5], "company": r[6]}
        for r in results
    ]
    return jsonify({"status": "ok", "results": employees})

# -------- MAIN ----------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
