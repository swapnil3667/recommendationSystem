import MySQLdb
import json

db = MySQLdb.connect("localhost","root","student","viki" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "SELECT user_id, video_id, score  FROM behavior_training"
cursor.execute(sql)
# Fetch all the rows in a list of lists.
results = cursor.fetchall()

d = {}
userid = []
videoid = []
userid_row = {}
videoid_col = {}
ur = 0
vc = 0
print "Came upto here "
print len(results)
count = 0
for data in results:
     user_id = data[0]
     video_id = data[1]
     score = data[2]
     rating = int(score.rstrip())


     count =  count+1;
     if rating > 2:
         if video_id in d:
              tempd = d[video_id]
              tempd[user_id] = score
              d[video_id] = tempd
         else:
              tempd = {}
              tempd[user_id] = score
              d[video_id] = tempd

     print count
     '''
     if count%10000 == 0:
          fileno = count/10000
          filename = "result" + str(fileno) + ".json"
          f = open(filename, 'w')
          jsonString = json.dumps(d, indent=4, sort_keys=True)
          f.write(jsonString)
          f.close()
    '''

print "finished"
f = open("video_id_relevant_rating_3_key.json", 'w')
jsonString = json.dumps(d, indent=4, sort_keys=True)
f.write(jsonString)
f.close()
