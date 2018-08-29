#!/usr/bin/env python
# coding=UTF-8
#from __future__ import unicode_literals
from elasticsearch import Elasticsearch
#import plac
#import random
from pathlib import Path
import spacy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# training data
print ("#FROM TO")
output_dir = "./model10iter"   
output_dir = Path(output_dir)
nlp = spacy.load(output_dir)  # load existing spaCy model

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
                    "field": "local"
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

            ],"should": [
            { "range": { "date" : { "from" : "2013-07-18 00:00:00", "to" : "2018-07-18 00:00:00" } }}
        ]
        }
    }
   }
res = es.search(index='twint', doc_type='items', body=doc,scroll='1m')
count = 0

while len(res) > 0:
#if True:
    scrollId = res['_scroll_id']
    #print (len(res),res['hits']['hits'])
    for doc in res['hits']['hits']:
        text = doc['_source']['tweet']
        doc_model = nlp(unicode(text))
        locs = []
        for ent in doc_model.ents:
            aux = (ent.start_char, ent.end_char, str(ent.label_))
            locs.append(text[ent.start_char:ent.end_char])
                
        print (doc['_id'],locs)
        es.update(index='twint',doc_type='items',id=doc['_id'], body={"doc": {"local": locs}})        
