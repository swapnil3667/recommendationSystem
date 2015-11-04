import pyhs2

with pyhs2.connect(host='localhost',
                   port=10000,
                   authMechanism="PLAIN",
                   user='root',
                   #password='',
                   database='viki') as conn:
    with conn.cursor() as cur:
        #Show databases
        print cur.getDatabases()

        #Execute query
        cur.execute("select * from user_attributes limit 1")

        #Return column info from query
#        print cur.getSchema()

        #Fetch table results
        for i in cur.fetch():
            print i
        userid = '109305'
        sql = "SELECT * FROM user_attributes where user_id=" + "'" + userid+"'"
        cur.execute(sql)
        # Fetch all the rows in a list of lists.
        results = cur.fetch()

        seed_userid = ""
        seed_country = ""
        seed_gender = ""
        for row in results:
            seed_userid = row[0]
            seed_country = row[1]
            seed_gender = row[2]
        sql = "SELECT user_id FROM user_attributes where country=" + "'" + seed_country+"' limit 200"
        cur.execute(sql)
               # Fetch all the rows in a list of lists.
        results = cur.fetch()
        d = {}
        userid = []
        videoid = []
        userid_row = {}
        videoid_col = {}
        ur = 0
        vc = 0
        print sql
        qr = ""
#        for row in results:
#            qr = qr + "or user_id='" + row[0] + "' "
#        query = "SELECT user_id,video_id, score FROM behavior_training where" + qr[2:]
#        print query

        for row in results:
            sql = "SELECT user_id,video_id, score FROM behavior_training where user_id=" + "'" + row[0]+"'"
            print row[0]

            cur.execute(sql)
            resultNew = cur.fetch()
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
