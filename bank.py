import mysql.connector
dataBase = mysql.connector.connect(
host ="localhost",
user ="root",
passwd ="12345678",
database = "management"
)

# preparing a cursor object
cursorObject = dataBase.cursor()

studentRecord = """
insert into hotel values(1,'rudy',)
"""

# table created
cursorObject.execute(studentRecord)
dataBase.commit()
# disconnecting from server
dataBase.close()
