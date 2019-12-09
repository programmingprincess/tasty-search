from flask import Flask, render_template, url_for, request, redirect
import random
import requests
import configparser
import json

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

@app.route('/')
def hello(name=None):
    return render_template('index.html', name=name)

@app.route('/results', methods=['GET'])
def results():

	pretty_query = request.args.get('query')
	pretty_query = pretty_query[1:-1]

	results = test

	return render_template('results.html', results=results, query=pretty_query)