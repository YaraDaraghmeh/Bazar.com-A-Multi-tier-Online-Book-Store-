from flask import Flask, jsonify, request
import csv
import os
import json


app = Flask(__name__)

DATA_FILE = "data/books.csv"
os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
