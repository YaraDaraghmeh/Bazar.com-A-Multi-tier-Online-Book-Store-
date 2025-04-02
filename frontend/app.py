from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

CATALOG_SERVICE_URL = "http://catalog:5000"
ORDER_SERVICE_URL = "http://order:5001"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search/<topic>', methods=['GET'])
def search(topic):
    response = requests.get(f"{CATALOG_SERVICE_URL}/search/{topic}")
    return jsonify(response.json())