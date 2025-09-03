
# Student Management System - Flask Web Backend
# Author: _Your Name_
# Description: RESTful API for managing student records with MySQL


import os
from flask import Flask, request, jsonify, render_template
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'default_secret')

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD'),
    'database': os.getenv('DB_NAME', 'student_db')
}

def get_connection():
    """Create and return a new database connection."""
    return mysql.connector.connect(**DB_CONFIG)

# ...existing code...

@app.route('/api/students/search', methods=['GET'])
def search_students():
    """Search students by name (case-insensitive substring match)."""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM students WHERE name LIKE %s', (f'%{query}%',))
        students = [
            dict(
                id=row[0],
                name=row[1],
                registration_number=row[2],
                date_of_birth=str(row[3]),
                age=row[4],
                gender=row[5],
                address=row[6],
                mobile_number=row[7],
                blood_group=row[8],
                marks=row[9]
            ) for row in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return jsonify(students)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """Render the main frontend page."""
    return render_template('index.html')


@app.route('/api/students', methods=['GET'])
def get_students():
    """Return all students as JSON."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM students')
        students = [
            dict(
                id=row[0],
                name=row[1],
                registration_number=row[2],
                date_of_birth=str(row[3]),
                age=row[4],
                gender=row[5],
                address=row[6],
                mobile_number=row[7],
                blood_group=row[8],
                marks=row[9]
            ) for row in cur.fetchall()
        ]
        cur.close()
        conn.close()
        return jsonify(students)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students', methods=['POST'])
def add_student():
    """Add a new student record."""
    data = request.json
    required = ['name', 'registration_number', 'date_of_birth', 'age', 'gender', 'address', 'mobile_number', 'blood_group', 'marks']
    if not data or not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO students (name, registration_number, date_of_birth, age, gender, address, mobile_number, blood_group, marks) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
            (
                data['name'],
                data['registration_number'],
                data['date_of_birth'],
                data['age'],
                data['gender'],
                data['address'],
                data['mobile_number'],
                data['blood_group'],
                data['marks']
            )
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Student added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    """Update student record except blood group and registration number."""
    data = request.json
    allowed = ['name', 'date_of_birth', 'age', 'gender', 'address', 'mobile_number', 'marks']
    fields = []
    values = []
    for k in allowed:
        if k in data:
            fields.append(f"{k}=%s")
            values.append(data[k])
    if not fields:
        return jsonify({'error': 'No updatable fields provided'}), 400
    try:
        conn = get_connection()
        cur = conn.cursor()
        query = f"UPDATE students SET {', '.join(fields)} WHERE id=%s"
        values.append(student_id)
        cur.execute(query, tuple(values))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Student updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    """Delete a student record."""
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('DELETE FROM students WHERE id=%s', (student_id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Student deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # For production, use Gunicorn or Waitress, not Flask's built-in server
    app.run(host='0.0.0.0', port=5000)
