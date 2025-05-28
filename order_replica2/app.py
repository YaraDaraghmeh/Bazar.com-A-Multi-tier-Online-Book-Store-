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


def get_next_catalog_url():
    global catalog_index
    url = catalog_replicas[catalog_index]
    catalog_index = (catalog_index + 1) % len(catalog_replicas)
    return url


@app.route('/purchase/<int:item_id>', methods=['POST'])
def purchase(item_id):
    catalog_url = get_next_catalog_url()
    response = requests.get(f"{catalog_url}/info/{item_id}")
    
    if response.status_code != 200:
        return jsonify({'error': 'Book not found'}), 404
    
    book_info = response.json()
    if book_info['quantity'] <= 0:
        return jsonify({'error': 'Book out of stock'}), 400
    
    #send invalidate request to frontend
    invalidate_response = requests.post(f"http://frontend:5002/invalidate/{item_id}")
    if invalidate_response.status_code != 200:
        return jsonify({'error': 'Failed to invalidate cache'}), 500

    #send update req to catalog
    update_url= f"http://catalog:5000/update/{item_id}"
    update_response = requests.put(
        update_url, 
        json={'quantity_change': -1},
        headers={'Content-Type': 'application/json'}
    )
    
    if update_response.status_code != 200:
        return jsonify({'error': 'Failed to update inventory'}), 500
    
    order_id = write_order(item_id)


    
    #update the order list in other replicas
   
    for replica_url in replica_urls:
        try:
            sync_data = {
            "id": order_id,
            "book_id": item_id,
            "timestamp": datetime.now().isoformat()
        }
            sync_resp = requests.post(f"{replica_url}/sync_order", json=sync_data)
            if sync_resp.status_code != 200:
                print(f"[Sync] Failed to sync with {replica_url}: {sync_resp.text}")
        except requests.RequestException as e:
            print(f"[Sync] Error syncing with {replica_url}: {e}")


    
    return jsonify({
        'status': 'success',
        'order_id': order_id,
        'book_title': book_info['title']
    })


@app.route('/sync_order', methods=['POST'])
def sync_order():
    data = request.get_json()
    if not data or 'id' not in data or 'book_id' not in data or 'timestamp' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    orders = read_orders()
    # Prevent duplicate orders
    if any(order['id'] == int(data['id']) for order in orders):
        return jsonify({'status': 'duplicate'}), 200

    with open(DATA_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data['id'], data['book_id'], data['timestamp']])

    return jsonify({'status': 'synced'}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006)