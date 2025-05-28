from flask import Flask, render_template, request, jsonify, make_response
import requests
import time

app = Flask(__name__)

# Round-robin index tracking
catalog_index = 0
order_index = 0

# Caches
SEARCH_CACHE_LIMIT = 10
def search_enforce_cache_limit(cache):
    while len(cache) > SEARCH_CACHE_LIMIT:
        # Remove the first inserted (oldest) item
        cache.pop(next(iter(cache)))

INFO_CACHE_LIMIT = 10
def info_enforce_cache_limit(cache):
    while len(cache) > INFO_CACHE_LIMIT:
        # Remove the first inserted (oldest) item
        cache.pop(next(iter(cache)))


search_topic_cache = {}
info_item_cache = {}


catalog_replicas = [
    "http://catalog:5000",
    "http://catalog_replica1:5003",
    "http://catalog_replica2:5004"
]

order_replicas = [
    "http://order:5001",
    "http://order_replica1:5005",
    "http://order_replica2:5006"
]

def get_next_catalog_url():
    global catalog_index
    url = catalog_replicas[catalog_index]
    catalog_index = (catalog_index + 1) % len(catalog_replicas)
    return url

def get_next_order_url():
    global order_index
    url = order_replicas[order_index]
    order_index = (order_index + 1) % len(order_replicas)
    return url

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/search/<topic>', methods=['GET'])
def search(topic):
    start = time.time()

    if topic in search_topic_cache:
        duration = time.time() - start
        resp = make_response(jsonify({
            "results": search_topic_cache[topic],
            "duration": duration
        }))
        resp.headers['X-Cache-Hit'] = 'true'
        return resp

    while True:
        catalog_url = get_next_catalog_url()
        try:
            response = requests.get(f"{catalog_url}/search/{topic}")
            result = response.json()
            if response.status_code == 200:
                search_topic_cache[topic] = result
                search_enforce_cache_limit(search_topic_cache)

            duration = time.time() - start
            print(f"[Search] Request to {catalog_url} took {duration:.4f} seconds")

            resp = make_response(jsonify({
                "results": result,
                "duration": duration
            }))
            resp.headers['X-Cache-Hit'] = 'false'
            return resp

        except requests.RequestException as e:
            print(f"[Search] Failed to reach {catalog_url}: {e}")
            continue


@app.route('/api/info/<int:item_id>', methods=['GET'])
def info(item_id):
    start = time.time()

    if item_id in info_item_cache:
        duration = time.time() - start
        resp = make_response(jsonify({
            "results": info_item_cache[item_id],
            "duration": duration
        }))
        resp.headers['X-Cache-Hit'] = 'true'
        return resp

    while True:
        catalog_url = get_next_catalog_url()
        try:
            response = requests.get(f"{catalog_url}/info/{item_id}")
            result = response.json()
            if response.status_code == 200:
                info_item_cache[item_id] = result
                info_enforce_cache_limit(info_item_cache)

            duration = time.time() - start
            print(f"[Info] Request to {catalog_url} took {duration:.4f} seconds")
            resp = make_response(jsonify({
                "results": result,
                "duration": duration
            }))
            resp.headers['X-Cache-Hit'] = 'false'
            return resp

        except requests.RequestException as e:
            print(f"[Info] Failed to reach {catalog_url}: {e}")
            continue


@app.route('/api/purchase/<int:item_id>', methods=['POST'])
def purchase(item_id):
    start = time.time()

    while True:
        order_url = get_next_order_url()
        try:
            response = requests.post(f"{order_url}/purchase/{item_id}")
            result = response.json()
            duration = time.time() - start
            print(f"[Purchase] Request to {order_url} took {duration:.4f} seconds")
            return jsonify({
                "results": result,
                "duration": duration
            }), response.status_code
        except requests.RequestException as e:
            print(f"[Purchase] Failed to reach {order_url}: {e}")
            continue


@app.route('/invalidate/<int:item_id>', methods=['POST'])
def invalidate(item_id):
    info_item_cache.pop(item_id, None)
    return jsonify({'status': 'success'}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5002)
