#!/usr/bin/python2

from flask import Flask, render_template, url_for, request, redirect
import random
import requests
import configparser
import json

import metapy

#import pyltr
import pickle
import sklearn

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

test = [{
	"title": "Paper 1",
	"abstract": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
	"keywords": ["paper", "abstract", "test"],
	"venue": "CHI",
	"numCitedBy": "10",
	"numKeyCitations": "5"

}, {
	"title": "Paper 2",
	"abstract": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
	"keywords": ["paper", "abstract", "test"],
	"venue": "CHI",
	"numCitedBy": "15",
	"numKeyCitations": "10"
}, {
	"title": "Paper 3",
	"abstract": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
	"keywords": ["paper", "abstract", "test", "information retrieval"],
	"venue": "CHI",
	"numCitedBy": "20",
	"numKeyCitations": "15"

}]

'''
	We have to read through latin1 because python2-->python3 encoding 

	sup_model: supervised LambdaMART model with 1000 estimators
					   trained on the training set given by search engine competition

	docs_info: dictionary of dictionaries. keyed by doc_id. contains:
					   paperAbstract, title, venue, numCitedBy, numKeyCitations, 
					   keyPhrases, numKeyReferences
'''

sup_model=""
with open(r"pickles/lamdamart_1000_0.02_50.pickle", "rb") as f:
		sup_model = pickle.load(f, encoding="latin1")

docs_info=""
with open(r"pickles/docs_info.pickle", "rb") as f:
		docs_info = pickle.load(f, encoding="latin1")

def model_predict(query):
	'''
	parameters
	- query: the query a user inputted 

	output
	- JSON of top X documents that are relevant to the query
		each doc json contains: paperAbstract, title, venue, numCitedBy, 
		numKeyCitations, keyPhrases, numKeyReferences


	TODO:
	- there may be multiple venues. right now we just take the first one
	'''

	test_x = get_features(query)
	print("Recieved features. Predicting...")
	pred = sup_model.predict(test_x)
	res=get_sorted_docs(pred, 10)

	res_dict = []
	for i in res:
		doc_id=i[0]
		# prettify the original dictionary values
		d={}
		d['title']=docs_info[doc_id]['title'][0]
		d['paperAbstract']=docs_info[doc_id]['paperAbstract'][0]
		d['venue']=docs_info[doc_id]['venue'][0]
		d['numCitedBy']=docs_info[doc_id]['numCitedBy'][0]
		d['numKeyCitations']=docs_info[doc_id]['numKeyCitations'][0]
		d['numKeyReferences']=docs_info[doc_id]['numKeyReferences'][0]
		d['keyPhrases']=docs_info[doc_id]['keyPhrases']

		res_dict.append(d)

	
	return json.dumps(res_dict)


def get_sorted_docs(test_pred, n):
	'''
	parameters
	- test_pred: document ranking scores by supervised model 
			(ordered by docs_info. iteration through dictionaries are stable)
	- n: the top N documents we want to return as a result

	output: 
	- list of (doc_id, score), sorted by top n 
	'''
	pred_dict = []

	# return the document associated with each score
	for idx, key in enumerate(docs_info):
		pred_dict.append([key, test_pred[idx]])	
	    
	my_scores = sorted(pred_dict, key = lambda x: x[1], reverse=True)

	return my_scores[:n]

def get_features(query):
	
	idx = metapy.index.make_inverted_index('config_academic.toml')
	ranker = metapy.index.OkapiBM25()
	ranker2 = metapy.index.AbsoluteDiscount()

	q = metapy.index.Document()
	q.content(query)
	
	score_bm25 = ranker.score(idx, q, num_results=8541)
	score_ad = ranker2.score(idx, q, num_results=8541)

	scores_bm25 = {}
	scores_ad = {}

	for score in range(len(score_bm25)):
		scores_bm25[idx.metadata(score_bm25[score][0]).get('id')] = score_bm25[score][1]
		scores_ad[idx.metadata(score_ad[score][0]).get('id')] = score_ad[score][1]

	res = []
	for doc in docs_info.keys():
		res.append([scores_b25[doc], scores_ad[doc], docs_info[doc]['numCitedBy'][0],docs_info[doc]['numKeyCitations'][0]])

	return res
	

@app.route('/')
def hello(name=None):
	model_predict("lol")
	return render_template('index.html', name=name)

@app.route('/results', methods=['GET'])
def results():

	# "pretty" removes the quotations at beginning and end of query
	pretty_query = request.args.get('query')
	pretty_query = pretty_query[1:-1]
	results = json.loads(model_predict(pretty_query))

	return render_template('results.html', results=results, query=pretty_query)
