#!/usr/bin/python

import MySQLdb



def f7(seq):
    seen = set()
    seen_add = seen.add
    return [ x for x in seq if not (x in seen or seen_add(x))]

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

       sql = "SELECT user_id FROM user_attributes where country=" + "'" + seed_country+"' LIMIT 200"
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
       for row in results:
           sql = "SELECT user_id,video_id, score FROM behavior_training where user_id=" + "'" + row[0]+"'"
         #  print row[0]
           cursor.execute(sql)
           resultNew = cursor.fetchall()
           for data in resultNew:
                user_id = data[0]
                video_id = data[1]
                score = data[2]

                if video_id not in videoid_col:
                    videoid_col[video_id] = vc
                    vc = vc+1

                if user_id not in userid_row:
                    userid_row[user_id] = ur
                    ur = ur+1

                if video_id not in videoid:
                    videoid.append(video_id)

                if user_id not in userid:
                    userid.append(user_id)

                if user_id in d:
                     tempd = d[user_id]
                     tempd[video_id] = score
                     d[user_id] = tempd
                     videoid.append(video_id)
                else:
                     tempd = {}
                     tempd[video_id] = score
                     d[user_id] = tempd


       #print d
       print 'Column Number of Video ID'
       print videoid_col

       print 'Row Number of User ID'
       print userid_row

       Sparse_Matrix = [[0 for x in range(len(videoid))] for x in range(len(userid))]
       for key in d:
        #   print key
           row_no = userid_row[key]
           tv_video = d[key]
         #  print tv_video
           for tvv in tv_video:
        #       print tvv
               col_no = videoid_col[tvv]
        #       print col_no
               Sparse_Matrix[row_no][col_no] = int(tv_video[tvv].rstrip())



      # print Sparse_Matrix
       for row in Sparse_Matrix:
           print row

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
