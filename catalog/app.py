from flask import Flask, jsonify, request
import csv
import os
import json
import requests

app = Flask(__name__)

DATA_FILE = "data/books.csv"
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)


if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'title', 'topic', 'quantity', 'price'])
        writer.writerow([1, 'How to get a good grade in DOS in 40 minutes a day', 'distributed systems', 10, 40])
        writer.writerow([2, 'RPCs for Noobs', 'distributed systems', 5, 50])
        writer.writerow([3, 'Xen and the Art of Surviving Undergraduate School', 'undergraduate school', 8, 30])
        writer.writerow([4, 'Cooking for the Impatient Undergrad', 'undergraduate school', 12, 25])


def read_books():
    books = []
    with open(DATA_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row['id'] = int(row['id'])
            row['quantity'] = int(row['quantity'])
            row['price'] = float(row['price'])
            books.append(row)
    return books

