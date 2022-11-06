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


cur.execute("CREATE TABLE reports (rid VARCHAR(200) NOT NULL PRIMARY KEY,user_email VARCHAR(30), r_date DATE ,category VARCHAR(10), r_long VARCHAR(20),r_lat VARCHAR(20), resolved Int);")
cnxn.commit()