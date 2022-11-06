##test updating resloved
import sqlite3



conn = sqlite3.connect('roadrage.db')
cur = conn.cursor()
id = "16a395f9-690d-45e4-9d8d-e767f529fed8"
##For given rid, set resolved to 1
cur.execute("UPDATE reports SET resolved = True WHERE rid = ?", (id,))
conn.commit()
conn.close()

##verify id was updated
conn = sqlite3.connect('roadrage.db')
cur = conn.cursor()
id = "3ec6fb2a-5ede-4de9-af2b-cb364d0f2c2f"
##check if resolved is 1
get_resolved = cur.execute("SELECT * FROM reports WHERE rid = ?", (id,)).fetchone()
conn.commit()
conn.close()
print(get_resolved)


## 