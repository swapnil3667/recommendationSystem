import MySQLdb

db = MySQLdb.connect("localhost","root","student","viki" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

  # Prepare SQL query to INSERT a record into the database.
sql = "SELECT user_id FROM behavior_training_new"
try:
 cursor.execute(sql)
 # Fetch all the rows in a list of lists.
 results = cursor.fetchall()
 for row in results:
     print row[0]
     sql = "SELECT country FROM user_attributes where user_id='"  + row[0] + "'"
     cursor.execute(sql)
     country = cursor.fetchone()
     sql = "Update behavior_training_new SET country='" + country[0].rstrip() + "' where user_id='" + row[0] +"'"


except Exception as ex:
 template = "An exception of type {0} occured. Arguments:\n{1!r}"
 message = template.format(type(ex).__name__, ex.args)
 print message
