from flask import Flask, jsonify, request
import csv
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

replica_urls = [
    "http://order_replica1:5005",
    "http://order:5001"
]
catalog_index = 0
catalog_replicas = [
    "http://catalog:5000",
    "http://catalog_replica1:5003",
    "http://catalog_replica2:5004"
]


DATA_FILE = "data/orders.csv"
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'book_id', 'timestamp'])




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)