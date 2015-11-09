import MySQLdb
import json

db = MySQLdb.connect("localhost","root","student","viki" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "SELECT *  FROM video_casts"
cursor.execute(sql)
# Fetch all the rows in a list of lists.
results = cursor.fetchall()

d =  {}
count = 0

for data in results:
     container_id = data[0]
     person_id = data[1]
     country = data[2]
     gender = data[3]

     count =  count+1;
     print count
     if container_id in d:
          tempd = d[container_id]
          tempd[person_id] = country + "_" + gender
          d[container_id] = tempd
     else:
          tempd = {}
          tempd[person_id] = country + "_" + gender
          d[container_id] = tempd

print "finished"
f = open("container_key.json", 'w')
jsonString = json.dumps(d, indent=4, sort_keys=True)
f.write(jsonString)
f.close()
