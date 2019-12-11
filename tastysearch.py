from flask import Flask, render_template, url_for, request, redirect
import random
import requests
import configparser
import json

import pyltr
import pickle
import sklearn

app = Flask(__name__)

test = [{
	"title": "Paper 1",
	"abstract": "Fake Abstract 1",
	"author": "John B. Doe",
	"keywords": ["paper", "abstract", "test"]
}, {
	"title": "Paper 2",
	"abstract": "Fake Abstract 2",
	"author": "John B. Doe II",
	"keywords": ["paper", "abstract", "test"]
}, {
	"title": "Paper 3",
	"abstract": "Fake Abstract 3",
	"author": "Jane A. Doe",
	"keywords": ["paper", "abstract", "test", "information retrieval"]
}]


# we have to read through latin1 because python2-->python3 encoding 
sup_model=""
with open(r"pickles/lamdamart_1000_0.02_50.pickle", "rb") as f:
		sup_model = pickle.load(f, encoding="latin1")

# docs= ""
# with open(r"pickles/docs.pickle", "rb") as f:
# 		docs = pickle.load(f, encoding="latin1")

docs_info=""
with open(r"pickles/docs_info_full.pickle", "rb") as f:
		docs_info = pickle.load(f, encoding="latin1")

def model_predict(query):
	'''
	parameters
	- query: the query a user inputted 

	output
	- list of top X documents that are relevant to the query
	'''
	test_x = get_features(query)
	pred = model.predict(test_x)

	print("Model_predict activated")
	print(docs_info)
	#sup_model.predict()
	return ""


def get_doc_list(test_pred, n):
	'''
	parameters
	- test_pred: document ranking scores by supervised model 
			(ordered by docs_info. iteration through dictionaries are stable)
	- n: the top N 
	'''
	# pred_dict = []

	# # return the document associated with each score
	# for idx, key in enumerate(docs_info):
	# 	pred_dict.append([key, test_pred[idx]])	
	    
 #  my_scores = sorted(pred_dict, key = lambda x: x[1], reverse=True)
 #  res = []

 #  for i in range(0,n):
 #      try:
 #          res = my_scores[i]        
 #          f.write(str(q_id) + "\t" + str(res[0]) + "\t" + str(res[1]) + "\n")
 #      except:
 #          pass

	# f.close()

def get_features(query):

	return "" 

@app.route('/')
def hello(name=None):
	model_predict("lol")
	return render_template('index.html', name=name)

@app.route('/results', methods=['GET'])
def results():

	pretty_query = request.args.get('query')
	pretty_query = pretty_query[1:-1]

	results = test

	return render_template('results.html', results=results, query=pretty_query)