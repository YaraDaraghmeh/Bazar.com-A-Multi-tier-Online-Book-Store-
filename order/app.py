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





@app.route('/purchase/<int:item_id>', methods=['POST'])
def purchase(item_id):
    catalog_url = f"http://catalog:5000/info/{item_id}"
    response = requests.get(catalog_url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Book not found'}), 404
    
    book_info = response.json()
    if book_info['quantity'] <= 0:
        return jsonify({'error': 'Book out of stock'}), 400
    
    update_url = f"http://catalog:5000/update/{item_id}"
    update_response = requests.put(
        update_url, 
        json={'quantity_change': -1},
        headers={'Content-Type': 'application/json'}
    )
    
    if update_response.status_code != 200:
        return jsonify({'error': 'Failed to update inventory'}), 500
    
    order_id = write_order(item_id)
    
    return jsonify({
        'status': 'success',
        'order_id': order_id,
        'book_title': book_info['title']
    })




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)