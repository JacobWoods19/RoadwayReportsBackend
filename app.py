import flask
from flask import request, jsonify
import json
from flask_cors import CORS, cross_origin
import uuid 
import mysql.connector
from mysql.connector.constants import ClientFlag
cnxn = mysql.connector.connect(**config)

app = flask.Flask(__name__)
CORS(app)
config = {
    'user': 'jacobwoods45',
    'password': '1234',
    'host': '94.944.94.94',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}
config['database'] = 'TigerHacks2022' 
cnxn = mysql.connector.connect(**config)
cur = cnxn.cursor() 

@app.route('/get_all_incidents')
def get_all_incidents():

    cur.execute("SELECT * FROM reports WHERE resolved = 0")
    ## convert to json
    rows = cur.fetchall()
    cnxn.commit()
    return jsonify(rows)
@app.route('/add_incident', methods= ['POST'])
def add_incident():
    date = request.args.get('date')
    incident_type = request.args.get('incident_type')
    long = request.args.get('long')
    lat = request.args.get('lat')
    email = request.args.get('email')
    cur.execute("INSERT INTO reports VALUES (?,?,?,?,?,?,?)", (str(uuid.uuid4()), date, incident_type, long, lat, email, 0))
    print(str(uuid.uuid4()), date, incident_type, long, lat, email, 0)
    cnxn.commit()
    return {"status": "success",
            "message": "Incident added successfully",
            "incident_type" : incident_type,
            "date" : date,
            "long" : long,
            "lat" : lat,
            "email" : email }
@app.route('/resolve_incident', methods= ['POST'])
def remove_incident():
    id = request.args.get('id')
    ##For given rid, set resolved to 1
    cur.execute("UPDATE reports SET resolved = 1 WHERE rid = ?", (id,))
    cnxn.commit()
    return {"status": "success",
            "message": "Incident removed successfully",
            "rid" : id}

@app.route('/add_user', methods= ['POST'])
def add_user():
    email = request.args.get('email')
    password = request.args.get('password')
    cur.execute("INSERT INTO users VALUES (?,?)", (email, password))
    cnxn.commit()
    return {"status": "success",
            "message": "User added successfully",
            "email" : email,
            "password" : password }

@app.route('/verify_user', methods= ['POST'])
def verify_user():
    email = request.args.get('email')
    password = request.args.get('password')
    get_password = cur.execute("SELECT u_password FROM users WHERE email = ?", (email,)).fetchone()
    cnxn.commit()
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
    cur.execute("""SELECT * FROM sqlite_master WHERE type='table' AND name='users'""")
    if cur.fetchone() is None:
        cur.execute("""CREATE TABLE users (email VARCHAR(30) NOT NULL UNIQUE,u_password VARCHAR(30) NOT NULL,PRIMARY KEY (email));""")
        cnxn.commit()
    cur.execute("""SELECT * FROM sqlite_master WHERE type='table' AND name='reports'""")
    if cur.fetchone() is None:
        cur.execute("CREATE TABLE reports (rid VARCHAR(200) NOT NULL PRIMARY KEY,user_email VARCHAR30, r_date DATE ,category VARCHAR(10) NOT NULL,r_long VARCHAR(20) NOT NULL,r_lat VARCHAR(20), resolved Int);")
        cnxn.commit()
    app.run(host="0.0.0.0", port = 8282)
