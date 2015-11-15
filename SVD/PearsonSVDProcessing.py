__author__ = 'sheenanasim'
#import scipy.sparse.linalg.svds as svd
import numpy as np
from scipy.sparse.linalg import eigen, svds as sparse_svd
import pprint
import time
import json
from scipy.stats import pearsonr

start_time = time.time()
# For printing the complete array values.
np.set_printoptions(threshold=np.inf)

#array1 = np.genfromtxt('/Users/sheenanasim/Documents/CS5228/project/knn.csv',delimiter = ",")
#print type(array1)
#print array1[1]
import pickle

userid = '9';
KNNType = 'Video';
filepath = '/Users/sheenanasim/Documents/CS5228/project/';


#with open('/Users/sheenanasim/Documents/CS5228/project/User_9/Location/KNN_9.out', 'r') as f:

with open(filepath+'User_'+userid+'/'+KNNType+"/KNN_"+userid+".out", 'r') as f:
    new_data = pickle.load(f)

with open(filepath+'User_'+userid+'/'+KNNType+'/'+userid+'.out', 'r') as f1:
    query = pickle.load(f1)
query1 = np.array(query)

svdInputMatrix = np.array(new_data,dtype=np.float)
svdInputList= []
for i in range(len(svdInputMatrix)):
    correlation,p = pearsonr(query1,svdInputMatrix[i])
    print "correlation = ", correlation
    if correlation > 0:
        svdInputList.append(svdInputMatrix[i])
#print array[1]

svdInputMatrixWithPearson = np.array(svdInputList,dtype=np.float)
print "new size after corelation check"
print type(svdInputMatrixWithPearson)
print svdInputMatrixWithPearson.shape
u,s,vt = sparse_svd(svdInputMatrixWithPearson)
"u,s,vt = sparse_svd(svdInputMatrix)"
print u.shape, s.shape, vt.shape
print s

energy = 0
for i in range(len(s)):
    energy = energy + (s[i]*s[i])
energy = (energy * 90)/100
print energy

V = np.transpose(vt)
print V.shape
print type(V)

result = np.dot(query1,V)
print result
print result.shape

fresult = np.dot(result,vt)
index = fresult.argsort()[-10:]

print index
descRecVideo = index[::-1].tolist()
print descRecVideo
print fresult[fresult.argsort()[-10:]]
print fresult[450]
print fresult[320]
print fresult[84]


with open(filepath+'User_'+userid+'/'+KNNType+'/videoid_col_'+userid+'.json', 'r') as videoIdFile:
    videoId = json.load(videoIdFile)
print type(videoId)

recVideosList = []
for i in range(len(descRecVideo)):
    val = descRecVideo[i]
    for key,value in videoId.iteritems():
        if value == val:
            recVideosList.insert(i,key)
            break

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
    #print key
    #print dictVideoViews.get(key);
    #sortedVideoList.index(i, dictVideoViews.get(key))
    sortedVideoList.append(dictVideoViews.get(key))

descRecVideo1 = sortedVideoList[::-1]


print sortedVideoList
  ##############Repetition code to rearrange according to no of views###############
with open(filepath+'User_'+userid+'/'+KNNType+'/videoid_col_'+userid+'.json', 'r') as videoIdFile1:
    videoId1 = json.load(videoIdFile1)
    print type(videoId1)

recVideosList1 = []
for i in range(len(descRecVideo1)):
    val = descRecVideo1[i]
    for key,value in videoId1.iteritems():
        if value == val:
            recVideosList1.insert(i,key)
            break

print recVideosList1

recVideosListFile = open(filepath+'User_'+userid+'/'+KNNType+'/user'+userid+'_Top10RecVideos.txt', 'w')
#pickle.dump(recVideosList,recVideosListFile)
for i in recVideosList:
    recVideosListFile.write(i+'\n')

end_time = time.time()

print "time in min =", (end_time - start_time)/60


