import csv
import sys

sys.stdout = open("KNN.txt", "w")
def Generate_KNN(userid,videoid):
	with open('/home/swapnil/Documents/KDD/20150701094451-Rakuten-Viki-Data/20150701094451-Behavior_training.csv', 'rb') as csvfile:
		lines = csv.reader(csvfile)
		dataset = list(lines)
		for x in range(len(dataset)-1):
			if(dataset[x][1] == userid):
				print dataset[x]
			if(dataset[x][2] == videoid):
                        	print dataset[x]


if __name__ == "__main__":
	with open('query.txt') as f:
    		content = f.readlines()
	userid = content[0]
	videoid = content[1]
	Generate_KNN(userid[:len(userid)-1],videoid[:len(videoid)-1])

