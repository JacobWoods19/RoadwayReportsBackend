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

##get all resolved reports and print them out
cur.execute("SELECT * FROM resolved_reports")
rows = cur.fetchall()
for row in rows:
    print(row)
cnxn.commit()