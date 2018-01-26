# -*- coding: utf-8 -*-
import oauth2
from time import gmtime, strftime
import json
from pprint import pprint

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
ACCESS_TOKEN = ""
ACCESS_TOKEN_SECRET = ""


def oauth_req(url, key, secret, http_method="GET", post_body="", http_headers=None):
    consumer = oauth2.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
    token = oauth2.Token(key=key, secret=secret)
    client = oauth2.Client(consumer, token)
    resp, content = client.request( url, method=http_method, body=post_body, headers=http_headers )
    return content

def get(usr):
	since ="944329492058853377"
	nome = usr+"_"+since+"_"+strftime("%Y-%m-%d_%H_%M_%S", gmtime())+".txt"
	file = open(nome,"w") 	 
	print(usr+'..................')
	#GET_TWEET_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='+usr+'&count=10'
	GET_TWEET_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name='+usr+'&count=200&max_id='+since
	print (GET_TWEET_URL)
	req = oauth_req(GET_TWEET_URL,ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
	print (str(req))
	file.write(str(req))  
	file.close() 
	return (nome)


def formato(nome):
	data = json.load(open(nome))
	file = open(nome+".tab","w") 	 

	for d in data:
		pprint(d['created_at'])
		pprint(d['id_str'])
		pprint(d['text'])
		print("")
		a = str(d['created_at']) + "\t" + d['id_str'] + "\t" + d['text'].replace("\n", " ; ") + "\n"
		file.write(a.encode('utf-8'))  

	file.close() 

if __name__ == '__main__':
	users = ['EPTC_POA']

	nome = get(users[0])
	formato(nome)
	
