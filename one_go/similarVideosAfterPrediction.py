import pickle
import json

def getSimilarVideos(videoid):
    with open('Similarity_Matrix.out', 'r') as f:
        new_data = pickle.load(f)


    query_video = videoid
    fobj = open("videoid_order.json", 'rU')
    #print "2"
    json_video_col = json.loads(fobj.read())

    row_col_no = json_video_col[query_video]

    size = len(json_video_col)
    #print size

    similar_videos = {}
    for i in range(size):
        if new_data[row_col_no][i] in similar_videos:
            li = similar_videos[new_data[row_col_no][i]]
            li.append(i)
            similar_videos[new_data[row_col_no][i]] = li
        else:
            li = []
            li.append(i)
            similar_videos[new_data[row_col_no][i]] = li

    #print similar_videos
    sorted(similar_videos, key=similar_videos.__getitem__, reverse=True)
    #print sorted(similar_videos.keys())
    rev = list(reversed(sorted(similar_videos.keys())))
    #print rev
    sort_by_video_col = {}

    for key in json_video_col:
        sort_by_video_col[json_video_col[key]] = key

    count=10
    reco_video = []
    for key in rev:
        li = similar_videos[key]
        for ids in li:
            video_name = sort_by_video_col[ids]
            reco_video.append(video_name)
            count = count -1
            if(count <0):
                break
        if( count < 0):
            break
    print reco_video

if __name__ == "__main__":
	with open('getSimilarVideo.txt') as f:
    		content = f.readlines()
	videoid = content[0]
	getSimilarVideos(videoid[:len(videoid)-1])
