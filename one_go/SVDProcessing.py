
import numpy as np
from scipy.sparse.linalg import eigen, svds as sparse_svd
import time
import json
import pickle

# Calculating program execution time
start_time = time.time()

# For printing the complete array values.
np.set_printoptions(threshold=np.inf)

#Creating File path, to read KNN values.
userid = '100004';
KNNType = 'Location';
filepath = '/Users/sheenanasim/Documents/CS5228/project/'

print 'userid = ',userid
print 'KNN Type = ',KNNType


with open(filepath+'User_'+userid+'/'+KNNType+"/KNN_"+userid+".out", 'r') as f:
    new_data = pickle.load(f)

#Reading query, row values of the userid to which recommendation has to be done.
with open(filepath+'User_'+userid+'/'+KNNType+'/'+userid+'.out', 'r') as f1:
    query = pickle.load(f1) 
query1 = np.array(query)

svdInputMatrix = np.array(new_data,dtype=np.float)
svdInputList= []
u,s,vt = sparse_svd(svdInputMatrix)
print u.shape, s.shape, vt.shape
print s

#Calculating energy for row elimination
energy = 0
for i in range(len(s)):
    energy = energy + (s[i]*s[i])
energy = (energy * 90)/100
print energy
#########################################


V = np.transpose(vt)
print V.shape

# Query * V
result = np.dot(query1,V)
print result
print result.shape

# ( Query * V) * V transpose
fresult = np.dot(result,vt)
#Finding the index of top most 10 values in fresult array.
index = fresult.argsort()[-10:]
print "Ascending order video coloumns"
print index

#Descending order list of videos (coloumn number) of high rating.
descRecVideo = index[::-1].tolist()
print "Descending order video coloumns"
print descRecVideo
print fresult[fresult.argsort()[-10:]]

#Finding video id values of coloumns
with open(filepath+'User_'+userid+'/'+KNNType+'/videoid_col_'+userid+'.json', 'r') as videoIdFile:
    videoId = json.load(videoIdFile)

recVideosList = []
for i in range(len(descRecVideo)):
    val = descRecVideo[i]
    for key,value in videoId.iteritems():
        if value == val:
            recVideosList.insert(i,key)
            break
print 'video id in desc order before sorting using no of views'
print recVideosList

#recVideosListFile = open(filepath+'User_'+userid+'/'+KNNType+'/user'+userid+'_Top10RecVideos.txt', 'w')

"""for i in recVideosList:
    recVideosListFile.write(i+'\n')"""


###Sorting the top 10 videos based on number of users who viewed it.
print "#####################sorting#########################"
dictVideoViews = {}
for i in descRecVideo:
    NoOfViews =0
    for row in range(svdInputMatrix.shape[0]):
        if svdInputMatrix[row][i] != 0:
            NoOfViews = NoOfViews + 1
    dictVideoViews[NoOfViews] = i

sortedVideoList = []

print sorted(dictVideoViews)

for key in sorted(dictVideoViews):
    sortedVideoList.append(dictVideoViews.get(key))

# col numbers of video in desc order.
descRecVideo1 = sortedVideoList[::-1]


##############Repetition code to rearrange according to no of views###############
with open(filepath+'User_'+userid+'/'+KNNType+'/videoid_col_'+userid+'.json', 'r') as videoIdFile1:
    videoId1 = json.load(videoIdFile1)

recVideosList1 = []
for i in range(len(descRecVideo1)):
    val = descRecVideo1[i]
    for key,value in videoId1.iteritems():
        if value == val:
            recVideosList1.insert(i,key)
            break

print 'decreasing order of rating'
print recVideosList1


recVideosListFile = open(filepath+'User_'+userid+'/'+KNNType+'/user'+userid+'_Top10RecVideos.txt', 'w')
for i in recVideosList1:
    recVideosListFile.write(i+'\n')

end_time = time.time()

print "time in min =", (end_time - start_time)/60 


