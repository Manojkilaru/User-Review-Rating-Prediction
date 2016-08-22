import json
import re
import unicodedata
import numpy as np
import nltk
import collections
import string
from sklearn import linear_model
from nltk.collocations import *


def unicodize(seg):
    if re.match(r'\\u[0-9a-f]{4}', seg):
        return seg.decode('unicode-escape')

    return seg.decode('utf-8')

y=''
bigram_measures = nltk.collocations.BigramAssocMeasures()
bag=[]
bigramBag=[]
bigramFreq=[]
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
	    y=y.replace('/',' ')
	    y=y.replace('\\',' ')
	    y=y.replace('\'',' ')
	    y=y.replace('"',' ')
	    y=re.split(r'[, .()"?!*#@()+:;%1234567890]',y)
	    if datanum%100 == 0:
	    	print datanum
	    for word in y:
	    	if(word.lower() not in bag):
	    		bag.append(word.lower())
    			frequency.append(int(1))
    		else:
		    	position=bag.index(word.lower())
		    	frequency[position]=frequency[position]+1

newbag=[]
for i in range(0,len(frequency)):
	if(frequency[i]>20):
		newbag.append(bag[i])
		
h=0

with open('finaldata.json') as fp:
	for line in fp:
	    if not line:  
	    	continue
	    data_obj = json.loads(line)
	    y=data_obj['text']
	    y=y.replace('\n',' ')
	    y=y.replace('-',' ')
	    y=y.replace('/',' ')
	    y=y.replace('\\',' ')
	    y=y.replace('\'',' ')
	    y=y.replace('"',' ')
	    y=re.split(r'[, .()"?!*#@()+:;%1234567890]',y)
	    forBiGrm=[]
	    h=h+1
	    for t in range(0,len(y)-1):
	    	if y[t].lower() in newbag:
	    		forBiGrm.append(y[t].lower()+' '+y[t+1].lower())
	    	else:
	    		if y[t+1].lower() in newbag:
	    			forBiGrm.append(y[t].lower()+' '+y[t+1].lower()) 
	    print h

	    '''
	    tempp=" ".join(map(str, y))#" ".join(str(item) for item in y)
	    tokens = nltk.wordpunct_tokenize(tempp.lower())
	    finder = BigramCollocationFinder.from_words(tokens)
	    scored = finder.score_ngrams(bigram_measures.raw_freq)
	    forBiGrm=sorted(bigram for bigram, score in scored)
	    print y
	    '''
	    for bword in forBiGrm:
	    	if bword.lower() not in bigramBag:
	    	    bigramBag.append(bword.lower())
	    	    bigramFreq.append(int(1))
	    	else:
	    	    position=bigramBag.index(bword.lower())
	    	    bigramFreq[position]=bigramFreq[position]+1
print len(bigramFreq)
print len(frequency)


newbag=[]
for i in range(0,len(frequency)):
	if(frequency[i]>20):
		newbag.append(bag[i])
print len(newbag)

x=[[0 for i in range(len(newbag)+len(bigramBag))] for j in range(datanum)]
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
	    y=y.replace('/',' ')
	    y=y.replace('\\',' ')
	    y=y.replace('\'',' ')
	    y=y.replace('"',' ')
	    y=re.split(r'[, .()"?!*#@()+:;%1234567890]',y)
	    for word in y:
	    	if word.lower() in newbag:
	    		column=newbag.index(word.lower())
	    		x[row][column]=x[row][column]+1
	    forBiGrm=[]
	    for t in range(0,len(y)-1):
	    	if y[t].lower() in newbag:
	    		forBiGrm.append(y[t]+' '+y[t+1])
	    	else:
	    		if y[t+1].lower() in newbag:
	    			forBiGrm.append(y[t]+' '+y[t+1]) 
	    for word in forBiGrm:
	    	if word.lower() in bigramBag:
	    		column=newbag.index(word.lower())
	    		x[row][column+len(newbag)]=x[row][column+len(newbag)]+1



clf = linear_model.LogisticRegression()
clf.fit(x, rating)




datanum=sum(1 for line in open('test.json'))
result=[[0 for i in range(1)] for j in range(datanum)]
x=[[0 for i in range(len(newbag)+len(bigramBag))] for j in range(datanum)]
row=-1
column=0
rating=[[0 for i in range(1)] for j in range(datanum)]
with open('test.json') as fp:
	for line in fp:
	    if not line:  
	    	continue
	    row=row+1;
	    data_obj = json.loads(line)
	    rating[row]=int(data_obj['stars'])
	    y=data_obj['text']
	    y=y.replace('\n',' ')
	    y=y.replace('-',' ')
	    y=y.replace('/',' ')
	    y=y.replace('\\',' ')
	    y=y.replace('\'',' ')
	    y=y.replace('"',' ')
	    y=re.split(r'[, .()"?!*#@()+:;%1234567890]',y)
	    for word in y:
	    	if word.lower() in newbag:
	    		column=newbag.index(word.lower())
	    		x[row][column]=x[row][column]+1
	    forBiGrm=[]
	    for t in range(0,len(y)-1):
	    	if y[t].lower() in newbag:
	    		forBiGrm.append(y[t]+' '+y[t+1])
	    	else:
	    		if y[t+1].lower() in newbag:
	    			forBiGrm.append(y[t]+' '+y[t+1]) 
	    for word in forBiGrm:
	    	if word.lower() in bigramBag:
	    		column=newbag.index(word.lower())
	    		x[row][column+len(newbag)]=x[row][column+len(newbag)]+1



result = clf.predict(x)
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


