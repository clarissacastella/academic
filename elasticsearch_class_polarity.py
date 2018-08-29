from elasticsearch import Elasticsearch
# coding=UTF-8
import collections
import nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier, MaxentClassifier, SklearnClassifier
import csv
from sklearn import cross_validation
from sklearn.svm import LinearSVC, SVC
import random
from nltk.corpus import stopwords
import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import *

from scipy.sparse import coo_matrix
from sklearn.utils import resample
import numpy as np

from nltk.metrics import scores

posdata = []
#with open('./data/positive-data.csv', 'rb') as myfile:    
with open('./data/gold/train_EPTC_POA_v3nbal_1.data', 'rb') as myfile:    
    reader = csv.reader(myfile, delimiter=',')
    for val in reader:
        posdata.append(val[0])        
 
negdata = []
#with open('./data/negative-data.csv', 'rb') as myfile:    
with open('./data/gold/train_EPTC_POA_v3nbal_0.data', 'rb') as myfile:    
    reader = csv.reader(myfile, delimiter=',')
    for val in reader:
        negdata.append(val[0])            

neudata = []
#with open('./data/negative-data.csv', 'rb') as myfile:    
with open('./data/gold/train_EPTC_POA_v3nbal_2.data', 'rb') as myfile:    
    reader = csv.reader(myfile, delimiter=',')
    for val in reader:
        neudata.append(val[0])


def word_split(data):    
    data_new = []
    for word in data:
        word_filter = [i.lower() for i in word.split()]
        data_new.append(word_filter)
    return data_new

def word_feats(words):    
    return dict([(word, words.count(word)) for word in words])
    
def chunkIt(seq, num):
    avg = len(seq) / float(num)
    out = []
    last = 0.0

    while last < len(seq):
        out.append(seq[int(last):int(last + avg)])
        last += avg

    return out    
    
def gettrainfeat(l, n):
	out = []
	for c in range(0,len(l)-1):
		if (c != n): 
			out = out + l[c]     
 	return out
 	

neudata = resample(neudata,n_samples=len(negdata))
posdata = resample(posdata,n_samples=len(negdata))

negfeats = [(word_feats(f), 'neg') for f in word_split(negdata)]
posfeats = [(word_feats(f), 'pos') for f in word_split(posdata)]
neufeats = [(word_feats(f), 'neu') for f in word_split(neudata)]

alldata = negdata + posdata + neudata
allfeats = negfeats + posfeats + neufeats       
    
classifier = SklearnClassifier(LinearSVC(), sparse=False)
classifier.train(allfeats)
 
es = Elasticsearch(['http://localhost:9200/'])
doc = {
        "query": {
        "bool": {
            "must_not":[ {
                "exists": {
                    "field": "likes"
                }
            },
             {
                "exists": {
                    "field": "replies"
                }
            },
             {
                "exists": {
                    "field": "retweets"
                }
            },
            {
                "exists": {
                    "field": "polarity"
                }
            },
            ],"should": [
            { "range": { "date" : { "from" : "2013-07-18 00:00:00", "to" : "2018-07-18 00:00:00" } }}
        ]
        }
    }
   }
res = es.search(index='twint', doc_type='items', body=doc,scroll='1m')
count = 0
print len(res)
while len(res) > 0:
#if True:
    scrollId = res['_scroll_id']
    print len(res),res['hits']['hits']
    #res = es.scroll(scroll_id = scrollId, scroll = '1m')
    print len(res)
    #quit()
    for doc in res['hits']['hits']:
        print doc['_id']
        cf = [(word_feats(f), '') for f in word_split([doc['_source']['tweet']])]
        observed = classifier.classify(cf[0][0])
        count = count + 1
        print(doc['_id'],observed,count)
        es.update(index='twint',doc_type='items',id=doc['_id'], body={"doc": {"polarity": observed}})
