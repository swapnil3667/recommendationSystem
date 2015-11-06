import MySQLdb
import json
import pickle

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

       sql = "SELECT user_id FROM user_attributes where country=" + "'" + seed_country+"' limit 2000"
       cursor.execute(sql)
              # Fetch all the rows in a list of lists.
       results = cursor.fetchall()
       json_data = {}
       print "1"
       fobj = open("result488.json", 'rU')
       print "2"
       json_data = json.loads(fobj.read())
       print "Finished up to here"
     #  print json_data["1"]

       userid = []
       videoid = []
       userid_row = {}
       videoid_col = {}
       ur = 0
       vc = 0
       print len(results)
       for row in results:
           user_id = row[0]
           if user_id in json_data:
               tv_video = json_data[user_id]
        #       print user_id
               print tv_video

               for tvvideo in tv_video:

                   if tvvideo not in videoid_col:
                       videoid_col[tvvideo] = vc
                       vc = vc+1

                   if user_id not in userid_row:
                       userid_row[user_id] = ur
                       ur = ur+1

                   if tvvideo not in videoid:
                       videoid.append(tvvideo)

                   if user_id not in userid:
                       userid.append(user_id)


       print len(videoid)
       print len(userid)
       Sparse_Matrix = [[0 for x in range(len(videoid))] for x in range(len(userid))]
       print len(Sparse_Matrix)
       print len(Sparse_Matrix[0])
       print videoid
       print userid
       for row in results:
           user_id = row[0]
           if user_id in json_data:
               tv_video = json_data[user_id]
               row_no = userid_row[user_id]
               for tvv in tv_video:
               #       print tvv
                  col_no = videoid_col[tvv]
               #       print col_no
                  Sparse_Matrix[row_no][col_no] = int(tv_video[tvv].rstrip())

       with open('result_user_9.out', 'w') as f:
           pickle.dump(Sparse_Matrix, f)
       for row in Sparse_Matrix:
          print row

    except Exception as ex:
        template = "An exception of type {0} occured. Arguments:\n{1!r}"
        message = template.format(type(ex).__name__, ex.args)
        print message
    db.close()

if __name__ == "__main__":
	with open('query.txt') as f:
    		content = f.readlines()
	userid = content[0]
	videoid = content[1]
	Generate_KNN(userid[:len(userid)-1])
