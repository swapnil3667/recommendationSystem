import MySQLdb
import json
import pickle

db = MySQLdb.connect("localhost","root","student","viki" )

# prepare a cursor object using cursor() method
cursor = db.cursor()


def unique(a):
    """ return the list with duplicate elements removed """
    return list(set(a))

def intersect(a, b):
    """ return the intersection of two lists """
    return list(set(a) & set(b))

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))



sql = "SELECT *  FROM video_attributes"
cursor.execute(sql)
# Fetch all the rows in a list of lists.
results = cursor.fetchall()

json_data = {}
print "1"
fobj = open("video_features_video_key.json", 'rU')
print "2"
json_data = json.loads(fobj.read())

video_row_col = {}
vc = 0
for data in results:
    video_id = data[0]
    video_row_col[video_id] = vc
    vc = vc+1

Similarity_Matrix = [[0 for x in range(len(video_row_col))] for x in range(len(video_row_col))]

f = open("videoid_order.json", 'w')
jsonString = json.dumps(video_row_col, indent=4, sort_keys=True)
f.write(jsonString)
f.close()

for data in results:
    video1 = data[0]
    for key in json_data:
        video2 = key
        if video2 != video1:
            col1 = video_row_col[video1]
            col2 = video_row_col[video2]
            if Similarity_Matrix[col1][col2] == 0 and Similarity_Matrix[col2][col1] == 0:
                intersection  = 0
                unions = 0
                video1_data  = json_data[video1]
                video2_data  = json_data[video2]
                if video1_data["adult"] == video2_data["adult"]:
                    intersection = intersection+1
                unions = unions +1
                if video1_data["content_owner_id"] == video2_data["content_owner_id"]:
                    intersection = intersection+1
                unions = unions +1
                if video1_data["origin_country"] == video2_data["origin_country"]:
                    intersection = intersection+1
                unions = unions +1
                if video1_data["origin_language"] == video2_data["origin_language"]:
                    intersection = intersection+1
                unions = unions +1

                if video1_data["cast"] != "None" and video2_data["cast"] != "None":
                    v1_cast = []
                    v2_cast = []
                    v1_dict = video1_data["cast"]
                    v2_dict = video2_data["cast"]
                #    print "Entering in Cast Condition"
                    for key in v1_dict:
                        v1_cast.append(key)

                    for key in v2_dict:
                        v2_cast.append(key)
                #    print v1_cast, v2_cast
                    vc1 = unique(v1_cast)
                    vc2 = unique(v2_cast)
                    commoncast = len(intersect(vc1,vc2))
                    totalcast = len(union(vc1,vc2))
                    print commoncast
                    if (commoncast) > 0:
                        intersection = intersection +1
        #                print "commoncast" , commomcast, totalcast
                    unions = unions +1

                if video1_data["genres"] != "None" and video2_data["genres"] != "None":
                    v1_genre = video1_data["genres"]
                    v2_genre = video2_data["genres"]
                    v1g = v1_genre.split(",")
                    v2g = v2_genre.split(",")

                    commongenre =  len(intersect(v1g,v2g))
                    totalgenre = len(union(v1g,v2g))
                    if (commongenre - totalgenre/3) > 0:
                        #print "commongenre" , commongenre , totalgenre
                        intersection = intersection +1
                    unions = unions +1

                #print intersection ,unions
                similarity = intersection*100/unions
                #print similarity
                Similarity_Matrix[col1][col2] = similarity
                Similarity_Matrix[col2][col1] = similarity


with open("Similarity_Matrix.out", 'w') as f:
   pickle.dump(Similarity_Matrix, f)
for row in Similarity_Matrix:
  print row
