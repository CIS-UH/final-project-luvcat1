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