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