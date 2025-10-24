from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import sqlite3
import os

# Flask App Setup
app = Flask(__name__, static_folder='frontend', static_url_path='')
CORS(app)

# -------------------------
# Database Setup
# -------------------------
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            designation TEXT NOT NULL,
            salary REAL NOT NULL,
            gender TEXT NOT NULL,
            address TEXT NOT NULL,
            company TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# -------------------------
# Serve Frontend (index.html)
# -------------------------
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# -------------------------
# Serve Static Files (JS/CSS)
# -------------------------
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# -------------------------
# API: Save Employee
# -------------------------
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    name = data.get('name')
    designation = data.get('designation')
    salary = data.get('salary')
    gender = data.get('gender')
    address = data.get('address')
    company = data.get('company')

    if not all([name, designation, salary, gender, address, company]):
        return jsonify({'status': 'error', 'message': 'All fields are required!'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO employees (name, designation, salary, gender, address, company)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (name, designation, salary, gender, address, company))
    conn.commit()
    conn.close()

    return jsonify({'status': 'success', 'message': f'Data saved for {name}'})

# -------------------------
# API: Search Employee
# -------------------------
@app.route('/search', methods=['GET'])
def search():
    field = request.args.get('field', 'name')
    value = request.args.get('value', '')

    if field not in ['name', 'company', 'designation']:
        return jsonify({'status': 'error', 'message': 'Invalid search field'}), 400

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM employees WHERE {field} LIKE ?", ('%' + value + '%',))
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return jsonify({'status': 'not_found', 'message': 'No records found!'})

    data = [
        {
            'id': r[0],
            'name': r[1],
            'designation': r[2],
            'salary': r[3],
            'gender': r[4],
            'address': r[5],
            'company': r[6]
        } for r in rows
    ]
    return jsonify({'status': 'success', 'results': data})

# -------------------------
# API: Get All Employees
# -------------------------
@app.route('/all', methods=['GET'])
def get_all():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employees")
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        return jsonify({'status': 'not_found', 'message': 'No employees found!'})

    data = [
        {
            'id': r[0],
            'name': r[1],
            'designation': r[2],
            'salary': r[3],
            'gender': r[4],
            'address': r[5],
            'company': r[6]
        } for r in rows
    ]
    return jsonify({'status': 'success', 'results': data})

# -------------------------
# Run the Server
# -------------------------
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)
