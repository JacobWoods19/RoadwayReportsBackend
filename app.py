import flask
from flask import request, jsonify
import json
from flask_cors import CORS, cross_origin
import uuid 
import mysql.connector
from mysql.connector.constants import ClientFlag
import datetime
from datetime import datetime

config = {
    'user': 'jacobwoods45',
    'password': '1234',
    'host': '35.232.112.164',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}

## create config file
cnxn = mysql.connector.connect(**config)

app = flask.Flask(__name__)
CORS(app)

config['database'] = 'TigerHacks22' 
cnxn = mysql.connector.connect(**config)
cur = cnxn.cursor(buffered=True) 

@app.route('/avg_response_time_by_category', methods=['GET'])
def avg_response_time_by_category():
    ##example resopnse
    ## [[category1, category2, category3], [avg_response_time1, avg_response_time2, avg_response_time3]]
    cur.execute("SELECT category, AVG(DATEDIFF(date_resolved, date_added)) FROM resolved_reports GROUP BY category;")
    result = cur.fetchall()
    categories = []
    avg_response_times = []
    for row in result:
        categories.append(row[0])
        avg_response_times.append(row[1])
    return jsonify([categories, avg_response_times])


@app.route('/get_average_response', methods=['GET'])
def get_average_response():
    ## givent a table of resolved reports, get the average bewteen the date added and date resolved for all reports
    cur.execute("SELECT * FROM resolved_reports")
    rows = cur.fetchall()
    print(rows)
    total = 0
    for row in rows:
        total += (row[3] - row[2]).days
    return jsonify({"average": int(total/len(rows))})

@app.route('/get_chart_data', methods=['GET'])
def get_chart_data():
    ##returns array of response times for each resolved report
    ## [ {date, response time}, {date, response time}, ...]
    cur.execute("SELECT * FROM resolved_reports")
    rows = cur.fetchall()
    print(rows)
    data = []
    for row in rows:
        data.append({"date": row[2], "response_time": (row[3] - row[2]).days})
    return jsonify(data)

@app.route('/get_reports_for_email', methods=['GET'])
def get_reports_for_email():
    ## given an email, return all reports for that email
    email = request.args.get('email')
    cur.execute("SELECT * FROM reports WHERE email = %s", (email,))
    rows = cur.fetchall()
    print(rows)
    return jsonify(rows)

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
    ## if date is not given, set date to current date
    if date == None:
        date = datetime.now()

    else:
        date = datetime.strptime(date, '%Y-%m-%d')
    incident_type = request.args.get('incident_type')
    long = request.args.get('long')
    lat = request.args.get('lat')
    email = request.args.get('email')
    cur.execute("INSERT INTO reports VALUES (%s,%s,%s,%s,%s,%s,%s)", (str(uuid.uuid4()), email, date, incident_type, long, lat, 0))
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
    ##For given rid, delete from reports
    ## Add resolved report to resolved_reports with type and date
    cur.execute("SELECT category, r_date FROM reports WHERE rid = %s", (id,))
    rows = cur.fetchall()
    category = rows[0][0]
    date = rows[0][1]
    ## Get today's date and time to pass into resolved_reports
    now = datetime.now()
    

    ##resolved_reports(rid VARCHAR(300), category VARCHAR (100), date_added DATE, date_resolved DATE
    cur.execute("INSERT INTO resolved_reports VALUES (%s,%s,%s,%s)", (id, category, date, now))

    cur.execute("DELETE FROM reports WHERE rid = %s;" , (id,))
    cnxn.commit()
    return {"status": "success",
            "message": "Incident removed successfully",
            "rid" : id}

@app.route('/add_user', methods= ['POST'])
def add_user():
    email = request.args.get('email')
    password = request.args.get('password')
    cur.execute("INSERT INTO users VALUES (%s,%s)", (email, password))
    cnxn.commit()
    return {"status": "success",
            "message": "User added successfully",
            "email" : email,
            "password" : password }

@app.route('/verify_user', methods= ['POST'])
def verify_user():
    email = request.args.get('email')
    password = request.args.get('password')
    cur.execute("SELECT u_password FROM users WHERE email = %s", (email,))
    rows = cur.fetchall()
    if len(rows) == 0:
        return {"status": "failure",
                "message": "User does not exist"}
    ## check if password is correct
    if rows[0][0] == password:
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
    app.run(host="0.0.0.0", port = 8282)
