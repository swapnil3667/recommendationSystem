import MySQLdb
import json
import pickle

def Generate_KNN(userid):
    # Open database connection
    db = MySQLdb.connect("localhost","root","student","viki" )

    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    query_user = userid


    fobj = open("video_id_relevant_rating_3_key.json", 'rU')
    print "2"
    json_video_data = json.loads(fobj.read())
    print "Finished up to here"
    fobj.close()
    fobj1 = open("result488.json", 'rU')
    print "2"
    json_data = json.loads(fobj1.read())
    print "Finished up to here"

    video_seen_by_user = []
    if query_user in json_data:
          tv_video = json_data[query_user]
          for tvv in tv_video:
              video_seen_by_user.append(tvv)

    userid = []
    videoid = []
    userid_row = {}
    videoid_col = {}
    ur = 0
    vc = 0

    results = []
    print  len(video_seen_by_user)
    np =0
    for video in video_seen_by_user:
        print np
        np = np +1
        if video in json_video_data:
            users = json_video_data[video]
#            print len(users)
            for key in users:
                results.append(key)



    print len(results)
    print "Reached Here"
    np = 0
    for user_id in results:
           #print np
           #np = np+1
           if user_id in json_data:
               tv_video = json_data[user_id]
        #       print user_id
        #       print tv_video

               for tvvideo in tv_video:

                  if tvvideo not in videoid_col:
                       videoid_col[tvvideo] = vc
                       vc = vc+1

                  if user_id not in userid_row:
                       userid_row[user_id] = ur
                       ur = ur+1
                  '''
                   if tvvideo not in videoid:
                       videoid.append(tvvideo)

                   if user_id not in userid:
                       userid.append(user_id)
                  '''
    print len(videoid_col)
    print len(userid_row)
    Sparse_Matrix = [[0 for x in range(len(videoid_col))] for x in range(len(userid_row))]
    print len(Sparse_Matrix)
    print len(Sparse_Matrix[0])
    #print videoid_col
    #print userid_row
    f = open("user_row_"+query_user+".json", 'w')
    jsonString = json.dumps(userid_row, indent=4, sort_keys=True)
    f.write(jsonString)
    f.close()
    f = open("videoid_col_"+query_user+".json", 'w')
    jsonString = json.dumps(videoid_col, indent=4, sort_keys=True)
    f.write(jsonString)
    f.close()

    for row in results:
       user_id = row
       if user_id in json_data:
           tv_video = json_data[user_id]
           row_no = userid_row[user_id]
           for tvv in tv_video:
           #       print tvv
              col_no = videoid_col[tvv]
           #       print col_no
              Sparse_Matrix[row_no][col_no] = int(tv_video[tvv].rstrip())
    queryuser = []

    for num in range(len(Sparse_Matrix[0])):
       queryuser.append(0)

    if query_user in json_data:
           tv_video = json_data[query_user]
           for tvv in tv_video:
               col_no = videoid_col[tvv]
               queryuser[col_no] = int(tv_video[tvv].rstrip())

    print "query user row", query_user
    print queryuser
    with open(query_user+".out", 'w') as f1:
       pickle.dump(queryuser, f1)
    outfile =  "KNN_" + query_user + ".out"
    with open(outfile, 'w') as f:
       pickle.dump(Sparse_Matrix, f)
    for row in Sparse_Matrix:
      print row

    db.close()

if __name__ == "__main__":
	with open('query.txt') as f:
    		content = f.readlines()
	userid = content[0]
	videoid = content[1]
	Generate_KNN(userid[:len(userid)-1])
