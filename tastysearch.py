from flask import Flask, render_template, url_for, request, redirect
import random
import requests
import configparser
import json

app = Flask(__name__)

@app.route('/')
def hello(name=None):
    return render_template('index.html', name=name)