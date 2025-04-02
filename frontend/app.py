from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

CATALOG_SERVICE_URL = "http://catalog:5000"
ORDER_SERVICE_URL = "http://order:5001"

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/api/info/<int:item_id>', methods=['GET'])
def info(item_id):
    response = requests.get(f"{CATALOG_SERVICE_URL}/info/{item_id}")
    return jsonify(response.json())