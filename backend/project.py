import flask
from flask import jsonify, request
import mysql.connector
from mysql.connector import Error
from datetime import datetime, date

#setting up an application name
app = flask.Flask(__name__) #sets up the application
app.config["DEBUG"] = True #allow to show errors in browser

def create_con(hostname, username, userpw, dbname):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname,
            user=username,
            password=userpw,
            database=dbname
        )
        print("connection successful\n")
    except Error as e:
        print(f'the error {e} occurred')
    return connection

DB_HOST = 'cis2368spring.cyzsyemwuyp7.us-east-1.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = '8Iw&6FxI'
DB_NAME = 'cis2368springdb'

# creates the connection to the MySQL database
db = create_con(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

# helper to convert date objects to strings for JSON serialization
def serialize_row(row):
    return {k: (v.isoformat() if isinstance(v, (datetime, date)) else v) for k, v in row.items()}

# homepage
@app.route('/')
def home():
    return jsonify({"message": "Flask API is running"})

def get_db():
    return mysql.connector.connect(
        host='cis2368spring.cyzsyemwuyp7.us-east-1.rds.amazonaws.com',
        user='admin',
        password='8Iw&6FxI',
        database='cis2368springdb'
    )

# ── MEMBERS ──────────────────────────────────────────────

# GET members API
@app.route('/members', methods=['GET'])
def get_members():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM member")
    members = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(members)

# POST members API
@app.route('/members', methods=['POST'])
def add_members():
    db = get_db()
    data = request.get_json(silent=True) or request.form

    name = data['name']
    details = data.get('details', '')
    title = data.get('title', '')
    level = data['level']

    cursor = db.cursor()
    query = """
    INSERT INTO member (name, details, title, level)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (name, details, title, level))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Member added successfully"})

# PUT members API
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    db = get_db()
    data = request.get_json(silent=True) or request.form

    cursor = db.cursor()
    query = """
    UPDATE member
    SET name=%s, details=%s, title=%s, level=%s
    WHERE id=%s
    """
    cursor.execute(query, (
        data['name'],
        data.get('details', ''),
        data.get('title', ''),
        data['level'],
        id
    ))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Member updated"})

# DELETE member API
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM member WHERE id=%s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Member deleted"})

# ── EVENTS ───────────────────────────────────────────────

# POST event API
@app.route('/events', methods=['POST'])
def add_event():
    db = get_db()
    data = request.get_json(silent=True) or request.form

    cursor = db.cursor()
    query = """
    INSERT INTO event (name, capacity, level, date)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(query, (
        data['name'],
        data['capacity'],
        data['level'],
        data['date']
    ))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Event created successfully"})

# GET events API
@app.route('/events', methods=['GET'])
def get_events():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM event")
    events = [serialize_row(e) for e in cursor.fetchall()]
    cursor.close()
    db.close()
    return jsonify(events)

# PUT events API
@app.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    db = get_db()
    data = request.get_json(silent=True) or request.form

    cursor = db.cursor()
    query = """
    UPDATE event
    SET name=%s, capacity=%s, level=%s, date=%s
    WHERE id=%s
    """
    cursor.execute(query, (
        data['name'],
        data['capacity'],
        data['level'],
        data['date'],
        id
    ))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Event updated successfully"})

# DELETE events API
@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM event WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Event deleted successfully"})

# ── REGISTRATIONS ────────────────────────────────────────

# POST registration API
@app.route('/registrations', methods=['POST'])
def add_registration():
    db = get_db()
    data = request.get_json(silent=True) or request.form

    cursor = db.cursor()
    query = """
    INSERT INTO registration (event_id, member_id)
    VALUES (%s, %s)
    """
    cursor.execute(query, (
        data['event_id'],
        data['member_id']
    ))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Registration successful"})

# GET registration API
@app.route('/registrations', methods=['GET'])
def get_registrations():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT id, event_id, member_id FROM registration")
    registrations = cursor.fetchall()
    cursor.close()
    db.close()
    return jsonify(registrations)

# DELETE registration API
@app.route('/registrations/<int:id>', methods=['DELETE'])
def delete_registration(id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM registration WHERE id = %s", (id,))
    db.commit()
    cursor.close()
    db.close()
    return jsonify({"message": "Registration deleted"})

if __name__ == '__main__':
    app.run()
