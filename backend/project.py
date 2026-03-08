import flask
from flask import jsonify, request
import mysql.connector
from mysql.connector import Error
from datetime import datetime

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

# all member API below

# GET members API
@app.route('/members', methods=['GET'])
def get_members():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM member")
    members = cursor.fetchall()
    return jsonify(members)

# POST members API that includes their name, details, title, and level
@app.route('/members', methods=['POST'])
def add_members():
    data = request.get_json()
    
    name = data['name']
    details = data['details']
    title = data['title']
    level = data['level']
    
    cursor = db.cursor()
    
    query = """
    INSERT INTO member (name, details, title, level)
    VALUES (%s, %s, %s, %s)
    """
    
    cursor.execute(query, (name, details, title, level))
    db.commit()
    return jsonify({"message": "Member added successfully"})
    
    
# PUT members API that updates a member's name, details, title, and/or level
@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    data = request.get_json()
    
    cursor = db.cursor()
    
    query = """
    UPDATE member
    SET name=%s, details=%s, title=%s, level=%s
    WHERE id=%s
    """
    
    cursor.execute(query, (
        data['name'],
        data['details'],
        data['title'],
        data['level'],
        id
    ))
    
    db.commit()
    
    return jsonify({"message": "Member updated"})

# DELETE member API if a member needs to be deleted from the database
@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    cursor = db.cursor()
    
    query = "DELETE FROM member WHERE id=%s"
    
    cursor.execute(query, (id,))
    db.commit()
    
    return jsonify({"message": "Member deleted"})
    
# all event API below

# POST event API to create events
@app.route('/events', methods=['POST'])
def add_event():
    data = request.get_json()
    
    cursor = db.cursor()
    
    query = """
    INSERT INTO event (id, name, capacity, level, date)
    VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor.execute(query, (
        data['name'],
        data['capacity'],
        data['level'],
        data['date']
    ))
    
    db.commit()
    
    return jsonify({"message": "Event created successfully"})

# GET events API to retrieve all events
@app.route('/events', methods=['GET'])
def get_events():
    cursor = db.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM event")
    
    events = cursor.fetchall()
    
    return jsonify(events)

# UPDATE events API to update existing events
@app.route('/events/<int:id>', methods=['PUT'])
def update_event(id):
    data = request.get_json()
    
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
    
    return jsonify({"message": "Event updated successfully"})

# DELETE events API to delete existing events
@app.route('/events/<int:id>', methods=['DELETE'])
def delete_event(id):
    cursor = db.cursor()
    
    cursor.execute("DELETE FROM event WHERE id = %s", (id,))
    
    db.commit()
    
    return jsonify({"message": "Event deleted successfully"})

# all registration API below

# POST registration API to create registration
@app.route('/registrations', methods=['POST'])
def add_registration():
    data = request.get_json()
    
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

    return jsonify({"message": "Registration successful"})

# GET registration API to view registration
@app.route('/registrations', methods=['GET'])
def get_registrations():
    cursor = db.cursor(dictionary=True)
    
    query = """
    SELECT
        registration.id,
        member.name AS member_name,
        event.name AS event_name,
        event.date
    FROM registration
    JOIN member ON registration.member_id = member.id
    JOIN event ON registration.event_id = event.id
    """
    
    cursor.execute(query)
    
    registrations = cursor.fetchall()
    
    return jsonify(registrations)

# DELETE registration API to cancel registration
@app.route('/registrations/<int:id>', methods=['DELETE'])
def delete_registration(id):
    cursor = db.cursor()
    
    cursor.execute("DELETE FROM registration WHERE id = %s", (id,))
    
    db.commit()
    
    return jsonify({"message": "Registration deleted"})

if __name__ == '__main__':
    app.run()