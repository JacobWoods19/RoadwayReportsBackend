import flask
from flask import request, jsonify
from flask_cors import CORS
import json
import sqlite3
import uuid 
from flask_cors import CORS

app = flask.Flask(__name__)
conn = sqlite3.connect('roadrage.db')
CORS(app)

@app.route('/get_all_incidents')
def get_all_incidents():
    conn = sqlite3.connect('roadrage.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM reports WHERE resolved = 0")
    ## convert to json
    rows = cur.fetchall()
    return jsonify(rows)
@app.route('/add_incident', methods= ['POST'])
def add_incident():
    conn = sqlite3.connect('roadrage.db')
    cur = conn.cursor()
    date = request.args.get('date')
    incident_type = request.args.get('incident_type')
    long = request.args.get('long')
    lat = request.args.get('lat')
    email = request.args.get('email')
    cur.execute("INSERT INTO reports VALUES (?,?,?,?,?,?,?)", (str(uuid.uuid4()), date, incident_type, long, lat, email, 0))
    conn.commit()
    return {"status": "success",
            "message": "Incident added successfully",
            "incident_type" : incident_type,
            "date" : date,
            "long" : long,
            "lat" : lat,
            "email" : email }
@app.route('/resolve_incident', methods= ['POST'])
def remove_incident():
    conn = sqlite3.connect('roadrage.db')
    cur = conn.cursor()
    id = request.args.get('id')
    ##For given rid, set resolved to 1
    cur.execute("UPDATE reports SET resolved = 1 WHERE id = ?", (id,))
    conn.commit()
    return {"status": "success",
            "message": "Incident removed successfully",
            "rid" : id}

@app.route('/add_user', methods= ['POST'])
def add_user():
    conn = sqlite3.connect('roadrage.db')
    cur = conn.cursor()
    email = request.args.get('email')
    password = request.args.get('password')
    cur.execute("INSERT INTO users VALUES (?,?)", (email, password))
    conn.commit()
    return {"status": "success",
            "message": "User added successfully",
            "email" : email,
            "password" : password }

@app.route('/verify_user', methods= ['POST'])
def verify_user():
    conn = sqlite3.connect('roadrage.db')
    cur = conn.cursor()
    email = request.args.get('email')
    password = request.args.get('password')
    get_password = cur.execute("SELECT u_password FROM users WHERE email = ?", (email,)).fetchone()
    ## check if password is correct
    if get_password[0] == password:
        return {"status": "success",
                "message": "User verified successfully",
                "email" : email,
                "password" : password }
    else:
        return {"status": "failure",
                "message": "User verification failed",
                "email" : email,
                "password" : password }

if __name__ == '__main__':
    conn = sqlite3.connect('roadrage.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM sqlite_master WHERE type='table' AND name='users'""")
    if cur.fetchone() is None:
        cur.execute("""CREATE TABLE users (email VARCHAR(30) NOT NULL UNIQUE,u_password VARCHAR(30) NOT NULL,PRIMARY KEY (email));""")
    cur.execute("""SELECT * FROM sqlite_master WHERE type='table' AND name='reports'""")
    if cur.fetchone() is None:
        cur.execute("CREATE TABLE reports (rid VARCHAR(30) NOT NULL PRIMARY KEY,user_email VARCHAR30, r_date DATE NOT NULL,category VARCHAR(10) NOT NULL,r_long VARCHAR(20) NOT NULL,r_lat VARCHAR(20), resolved BIT);")
    app.run(host="0.0.0.0")
