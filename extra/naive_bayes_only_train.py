import json
import re
import numpy as np
from sklearn.naive_bayes import MultinomialNB
y=''
bag=[]
frequency=[]
datanum=0
with open('finaldata.json') as fp:
	for line in fp:
	    if not line:  
	    	continue
	    datanum=datanum+1;
	    data_obj = json.loads(line)
	    y=data_obj['text']
	    y=y.replace('\n',' ')
	    y=y.replace('-',' ')
	    y=re.split(r'[, .()"?!*#@\()+:;%/1234567890]',y)
	    for word in y:
	    	if(word.lower() not in bag):
	    		bag.append(word.lower())
    			frequency.append(int(1))
    		else:
		    	position=bag.index(word.lower())
		    	frequency[position]=frequency[position]+1

#print frequency
#print len(frequency)
newbag=[]
for i in range(0,len(frequency)):
	if(frequency[i]>20):
		newbag.append(bag[i])
print len(newbag)
x=[[0 for i in range(len(newbag))] for j in range(datanum)]
row=-1
column=0
rating=[[0 for i in range(1)] for j in range(datanum)]
with open('finaldata.json') as fp:
	for line in fp:
	    if not line:  
	    	continue
	    row=row+1;
	    data_obj = json.loads(line)
	    rating[row]=int(data_obj['stars'])
	    y=data_obj['text']
	    y=y.replace('\n',' ')
	    y=y.replace('-',' ')
	    y=re.split(r'[, .()"?!*#@\()+:;%/1234567890]',y)
	    for word in y:
	    	if word.lower() in newbag:
	    		column=newbag.index(word.lower())
	    		x[row][column]=x[row][column]+1

clf = MultinomialNB()
clf.fit(x, rating)
result=[[0 for i in range(1)] for j in range(datanum)]
result = clf.predict(x)
#mse = ((result - rating) ** 2).mean(axis=ax)
from sklearn.metrics import mean_squared_error
from math import sqrt
rms = sqrt(mean_squared_error(rating, result))
error = rms/5
error_percentage = error*100
accuracy_percentage = 100 - error_percentage
print accuracy_percentage