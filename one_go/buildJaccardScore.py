import pickle
import json

def buildJaccardScore(userid):
    with open('Similarity_Matrix.out', 'r') as f:
        new_data = pickle.load(f)

    #print new_data

    fobj = open("videoid_order.json", 'rU')
    print "2"
    json_video_col = json.loads(fobj.read())


    fobj1 = open("/home/swapnil/Documents/KDD/viki_recommendation/behavior_training.json", 'rU')
    print "2"
    json_data = json.loads(fobj1.read())
    print "Finished up to here"

    query_user=userid
    video_seen_by_user = []
    if query_user in json_data:
          tv_video = json_data[query_user]
          for tvv in tv_video:
              video_seen_by_user.append(tvv)

    print video_seen_by_user


    test_video = []
    with open("/home/swapnil/Documents/KDD/viki_recommendation/Results/User_9/user_9_submisison.txt") as inputfile:
        for line in inputfile:
            test_video.append(line.strip())

    rc_video = []
    with open('/home/swapnil/Documents/KDD/viki_recommendation/Results/User_9/Video/user9_Top10RecVideos.txt') as inputfile:
        for line in inputfile:
            rc_video.append(line.strip())
    json_test_score = {}
    json_recc_score = {}
    for video in video_seen_by_user:
        print video
        col1 = json_video_col[video]

        print  "score of testing videos"
        t1 = {}
        for test in test_video:
            col2 = json_video_col[test]
            t1[test] = new_data[col1][col2]
            print test, new_data[col1][col2]

        print  "score of recommended videos"
        t2 = {}
        for test in rc_video:
            col2 = json_video_col[test]
            print test, new_data[col1][col2]
            t2[test] = new_data[col1][col2]

        json_test_score[video] = t1
        json_recc_score[video] = t2

    f = open("jaccard_test_score_"+query_user+".json", 'w')
    jsonString = json.dumps(json_test_score, indent=4, sort_keys=True)
    f.write(jsonString)
    f.close()

    f = open("jaccard_recc_score_"+query_user+".json", 'w')
    jsonString = json.dumps(json_recc_score, indent=4, sort_keys=True)
    f.write(jsonString)
    f.close()


if __name__ == "__main__":
	with open('query.txt') as f:
    		content = f.readlines()
	userid = content[0]
	buildJaccardScore(userid[:len(userid)-1])