from flask import Flask, render_template, url_for, request, redirect
import random
import requests
import configparser
import json

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

@app.route('/')
def hello(name=None):
    return render_template('index.html', name=name)

@app.route('/results', methods=['GET'])
def results():

	pretty_query = request.args.get('query')
	pretty_query = pretty_query[1:-1]

	results = test

	return render_template('results.html', results=results, query=pretty_query)
