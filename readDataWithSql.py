#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","student","viki" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Prepare SQL query to INSERT a record into the database.
sql = "SELECT * FROM behavior_training \
       LIMIT 1 "
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      fname = row[0]
      lname = row[1]
      age = row[2]
      sex = row[3]
      income = row[4]
      # Now print fetched result
      print "date=%s,user_id=%s,videoid=%s,mv_ratio=%s,rating=%s" % \
             (fname, lname, age, sex, income )

   sql = "CREATE VIEW V AS SELECT behavior_training.user_id, behavior_training.video_id, \
           user_attributes.country, user_attributes.gender, score, origin_country, genres, \
           person_id, video_casts.country as cast_country , video_casts.gender as cast_gender \
           FROM (((behavior_training INNER JOIN user_attributes) \
           INNER JOIN  video_attributes) INNER JOIN video_casts)"

   cursor.execute(sql)

   sql = "SELECT * FROM V \
           LIMIT 1 "

   cursor.execute(sql)
   # Fetch all the rows in a list of lists.
   results = cursor.fetchall()
   for row in results:
      user_id = row[0]
      video_id = row[1]
      country = row[2]
      gender = row[3]
      score = row[4]
      origin_country = row[5]
      genre = row[6]
      person_id = row[7]
      cast_country = row[8]
      cast_gender = row[9]

      # Now print fetched result
      print "user_id=%s,videoid=%s,country=%s,gender=%s,score=%s,origin_country=%s,genre=%s,person_id=%s,cast_country=%s,cast_gender=%s" % \
             (user_id, video_id, country, gender, score, origin_country, genre, person_id, cast_country, cast_gender )

   sql = "DROP VIEW V"
   cursor.execute(sql)

except Exception as ex:
    template = "An exception of type {0} occured. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print message

#except:
 #  print "Error: unable to fecth data"


# disconnect from server

db.close()
