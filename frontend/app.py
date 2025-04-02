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

@app.route('/api/info/<int:item_id>', methods=['GET'])
def info(item_id):
    response = requests.get(f"{CATALOG_SERVICE_URL}/info/{item_id}")
    return jsonify(response.json())

@app.route('/api/purchase/<int:item_id>', methods=['POST'])
def purchase(item_id):
    response = requests.post(f"{ORDER_SERVICE_URL}/purchase/{item_id}")
    return jsonify(response.json()), response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)