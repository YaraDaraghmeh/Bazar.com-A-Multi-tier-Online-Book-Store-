from flask import Flask, jsonify, request
import csv
import os
import requests
import json
from datetime import datetime

app = Flask(__name__)

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