from flask import Flask, jsonify, request
import csv
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

replica_urls = [
    "http://order:5001",
    "http://order_replica2:5006"
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

def read_orders():
    orders = []
    with open(DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['id'] = int(row['id'])
            row['book_id'] = int(row['book_id'])
            orders.append(row)
    return orders

def write_order(book_id):
    orders = read_orders()
    new_id = 1
    if orders:
        new_id = max(order['id'] for order in orders) + 1
    
    with open(DATA_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([new_id, book_id, datetime.now().isoformat()])
    return new_id

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)