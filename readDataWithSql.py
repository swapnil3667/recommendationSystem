#!/usr/bin/python

import MySQLdb


def Generate_KNN(userid):
    # Open database connection
    db = MySQLdb.connect("localhost","root","student","viki" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "SELECT * FROM user_attributes where user_id=" + "'" + userid+"'"
    try:
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       results = cursor.fetchall()

       seed_userid = ""
       seed_country = ""
       seed_gender = ""
       for row in results:
           seed_userid = row[0]
           seed_country = row[1]
           seed_gender = row[2]
       wh = "";
       if(seed_userid!="" and seed_country!="" and seed_gender!="") :
           wh ="seed_userid ='" +seed_userid +"' and"+ " seed_country ='" +seed_country +"' and"+ " seed_gender ='" +seed_gender +"'"
       elif(seed_userid==""):
          wh = "seed_country ='" +seed_country +"' and"+ " seed_gender ='" +seed_gender + "'"
       elif(seed_country==""):
          wh = "seed_userid ='" +seed_userid +"' and"+ " seed_gender ='" +seed_gender + "'"
       elif(seed_gender==""):
         wh = "seed_country ='" +seed_country +"' and"+" seed_country ='" +seed_country +"'"

       print wh
       print seed_userid, seed_country, seed_gender

       sql = "CREATE VIEW V AS SELECT behavior_training.user_id, behavior_training.video_id, \
               user_attributes.country, user_attributes.gender, score, origin_country, genres, \
               person_id, video_casts.country as cast_country , video_casts.gender as cast_gender \
               FROM (((behavior_training INNER JOIN user_attributes) \
               INNER JOIN  video_attributes) INNER JOIN video_casts)"

       print sql

       cursor.execute(sql)

       sql = "SELECT * FROM V where user_id='" + seed_userid  + "' or country='" + seed_country + "' or gender='" + seed_gender + "'"
       print "After this"
       cursor.execute(sql)
       # Fetch all the rows in a list of lists.
       print "After it"
       d = {}
       results = cursor.fetchall()
       print "Finally"
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

          if seed_userid == user_id or seed_country == country or seed_gender == gender:
              if user_id in d:
                  tempd = d[user_id]
                  tempd[video_id] = score
                  d[user_id] = tempd
              else:
                  tempd = {}
                  tempd[video_id] = score
                  d[user_id] = tempd
          print user_id
          print country

          # Now print fetsched result
          #print "user_id=%s,videoid=%s,country=%s,gender=%s,score=%s,origin_country=%s,genre=%s,person_id=%s,cast_country=%s,cast_gender=%s" % \
            #     (user_id, video_id, country, gender, score, origin_country, genre, person_id, cast_country, cast_gender )

       print d
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

if __name__ == "__main__":
	with open('query.txt') as f:
    		content = f.readlines()
	userid = content[0]
	videoid = content[1]
	Generate_KNN(userid[:len(userid)-1])
