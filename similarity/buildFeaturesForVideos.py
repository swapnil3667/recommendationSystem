import MySQLdb
import json

db = MySQLdb.connect("localhost","root","student","viki" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

sql = "SELECT *  FROM video_attributes"
cursor.execute(sql)
# Fetch all the rows in a list of lists.
results = cursor.fetchall()

json_data = {}
print "1"
fobj = open("container_key.json", 'rU')
print "2"
json_data = json.loads(fobj.read())
d =  {}
count = 0
for data in results:
     video_id = data[0]
     container_id = data[1]
     origin_country = data[2]
     origin_language = data[3]
     adult =  data[4]
     broadcast_from = data[5]
     broadcast_to = data[6]
     season_number = data[7]
     content_owner_id = data[8]
     genres = data[9]
     episodes_count = data[10]

     count =  count+1;
     print count
     if video_id in d:
          tempd = d[video_id]
          tempd["origin_country"] = origin_country
          tempd["origin_language"] = origin_language
          tempd["adult"] = adult
          tempd["content_owner_id"] = content_owner_id
          tempd["genres"] = genres
          if container_id in json_data:
              tempd["cast"] = json_data[container_id]
          else:
              tempd["cast"] = "None"

          d[video_id] = tempd
     else:
          tempd = {}
          tempd["origin_country"] = origin_country
          tempd["origin_language"] = origin_language
          tempd["adult"] = adult
          tempd["content_owner_id"] = content_owner_id
          tempd["genres"] = genres
          if container_id in json_data:
              tempd["cast"] = json_data[container_id]
          else:
              tempd["cast"] = "None"
          d[video_id] = tempd


print "finished"
f = open("video_features_video_key.json", 'w')
jsonString = json.dumps(d, indent=4, sort_keys=True)
f.write(jsonString)
f.close()
