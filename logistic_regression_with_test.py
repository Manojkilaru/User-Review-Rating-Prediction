import json
import re
import numpy as np
from sklearn import linear_model
import csv
#y is iterated over all the reviews
y=''
#bag contains all the words present among the reviews
bag=[]
#frequency contains the frequencies of wach word in the bag
frequency=[]
#datanum is the serial number of the review
datanum=0
#Opening the train file
with open('finaldata.json') as fp:
	#iterating over the data of each person
	for line in fp:
		#if there is an empty line, ignore it
	    if not line:  
	    	continue
	    datanum=datanum+1;
	    #load the data from the json file
	    data_obj = json.loads(line)
	    #extract only the text review portion of the data
	    y=data_obj['text']
	    #remove the newline characters from the reviews
	    y=y.replace('\n',' ')
	    #remove the hyphens from the reviews
	    y=y.replace('-',' ')
	    #splitting the data into individual words
	    y=re.split(r'[, .()"?!*#@\()+:;%/1234567890]',y)
	    #collecting the words from the reviews
	    for word in y:
	    	#if the word is not already in the bag, we add it
	    	if(word.lower() not in bag):
	    		bag.append(word.lower())
	    		#The frequency of the word added is made 1
    			frequency.append(int(1))
    		#if the word is already in the bag
    		else:
		    	position=bag.index(word.lower())
		    	#The frequency is increased by one
		    	frequency[position]=frequency[position]+1

#print frequency
#print len(frequency)
#newbag contains the words we include in the feature vector
newbag=[]
for i in range(0,len(frequency)):
	#The words that have frequency less than 5 are not considered
	if(frequency[i]>20):
		newbag.append(bag[i])

#print len(newbag)
#X is the final feature vector constructed from the train data
x=[[0 for i in range(len(newbag))] for j in range(datanum)]
#row is the number of the row in the data
row=-1
#column is the number of the column
column=0
#rating is the output column
rating=[[0 for i in range(1)] for j in range(datanum)]
with open('finaldata.json') as fp:
	for line in fp:
	    if not line:  
	    	continue
	    row=row+1;
	    #load the data from the json file
	    data_obj = json.loads(line)
	    #extract only the rating portion of the data
	    rating[row]=int(data_obj['stars'])
	    #extract only the text review portion of the data
	    y=data_obj['text']
	    y=y.replace('\n',' ')
	    y=y.replace('-',' ')
	    y=re.split(r'[, .()"?!*#@\()+:;%/1234567890]',y)
	    #collecting the words from the review
	    for word in y:
	    	#We consider only the words that are in the features collection
	    	if word.lower() in newbag:
	    		column=newbag.index(word.lower())
	    		x[row][column]=x[row][column]+1

#Applying logistic regression to the data
clf = linear_model.LogisticRegression()
#Fitting the train data into the logistic regression
clf.fit(x, rating)
#datanum is the number of lines in the test data
datanum=sum(1 for line in open('test.json'))
#result is the final ratings of the test data
result=[[0 for i in range(1)] for j in range(datanum)]
#X is the final feature vector constructed from the test data
x=[[0 for i in range(len(newbag))] for j in range(datanum)]
row=-1
column=0
#rating is the original ratings of thetest data
rating=[[0 for i in range(1)] for j in range(datanum)]
#Opening the test data
with open('test.json') as fp:
	for line in fp:
	    if not line:  
	    	continue
	    row=row+1;
	    #load the data from the json file
	    data_obj = json.loads(line)
	    #extract only the rating portion of the data
	    rating[row]=int(data_obj['stars'])
	    #extract only the text review portion of the data
	    y=data_obj['text']
	    y=y.replace('\n',' ')
	    y=y.replace('-',' ')
	    y=re.split(r'[, .()"?!*#@\()+:;%/1234567890]',y)
	    #collecting the words from the review
	    for word in y:
	    	#We consider only the words that are in the features collectio
	    	if word.lower() in newbag:
	    		column=newbag.index(word.lower())
	    		x[row][column]=x[row][column]+1
#result is predicted from the feature vector constructed from train data using logistic regression
result = clf.predict(x)


with open('output.csv', 'wt') as out:
    csv_writer = csv.writer(out)
    S = []
    S.append('Id')
    S.append('Rating')
    csv_writer.writerow(S)
    for i in range(len(result)):
        line= []
        line.append(i)
        if int(round(result[i]))<=0:
        	line.append(1)
        elif int(round(result[i]))>=6:
        	line.append(5)
        else:
        	line.append(int(round(result[i])))
        csv_writer.writerow(line)

#print result 
#print rating
#mse = ((result - rating) ** 2).mean(axis=ax)
from sklearn.metrics import mean_squared_error
from math import sqrt
rms = sqrt(mean_squared_error(rating, result))
error = rms/5
error_percentage = error*100
accuracy_percentage = 100 - error_percentage
print accuracy_percentage