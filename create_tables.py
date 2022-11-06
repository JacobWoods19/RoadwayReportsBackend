import mysql.connector
from mysql.connector.constants import ClientFlag
config = {
    'user': 'jacobwoods45',
    'password': '1234',
    'host': '35.232.112.164',
    'client_flags': [ClientFlag.SSL],
    'ssl_ca': 'ssl/server-ca.pem',
    'ssl_cert': 'ssl/client-cert.pem',
    'ssl_key': 'ssl/client-key.pem'
}
config['database'] = 'TigerHacks22' 
## create config file
cnxn = mysql.connector.connect(**config)
cnxn = mysql.connector.connect(**config)
cur = cnxn.cursor() 

# cur.execute("CREATE TABLE resolved_reports(rid VARCHAR(300), category VARCHAR (100), date_added DATE, date_resolved DATE);")


# # insert user
# cur.execute("INSERT INTO users (email, u_password) VALUES (%s, %s)", ("user", "password"))

## describe reports table
cur.execute("DESCRIBE reports")
rows = cur.fetchall()
print(rows)


cnxn.commit()