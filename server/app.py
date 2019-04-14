import os
from bson import json_util, ObjectId

# import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS

from flask import Flask, render_template, redirect, url_for, request, jsonify
from pymongo import MongoClient
import requests, json

# Making connection to locally hosted MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.northpark

collist = db.list_collection_names()
if "books" in collist:
    db.books.drop()

BOOKS = db["books"]

with open("books.json") as f:
    booksdata = json.load(f)
BOOKS.insert_many(booksdata)

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        print(post_data)
        print("la")
        new_item = {
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
            'price': post_data.get('price')
        }
        print(new_item)
        BOOKS.insert_one(new_item)
        response_object['message'] = 'Book added!'
    else:
        pymongo_cursor = BOOKS.find()
        all_books = list(pymongo_cursor)
        for i in all_books:
            i["_id"] = str(i["_id"])
        response_object['books'] = all_books
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'GET':
        # TODO: refactor to a lambda and filter
        return_book = ''
        obj = BOOKS.find_one({'_id': ObjectId(book_id)})
        obj["_id"] = str(i["_id"])
        response_object['book'] = obj
    if request.method == 'PUT':
        post_data = request.get_json()
        BOOKS.delete_one({ "_id":ObjectId(book_id)})
        new_item = {
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
            'price': post_data.get('price')
        }
        BOOKS.insert_one(new_item)
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        BOOKS.delete_one({ "_id":ObjectId(book_id)})
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


@app.route('/charge', methods=['POST'])
def create_charge():
    response_object = {
        'status': 'success',
        'charge': 0
    }
    return jsonify(response_object), 200


@app.route('/charge/<charge_id>')
def get_charge(charge_id):
    response_object = {
        'status': 'success',
        'charge': 0
    }
    return jsonify(response_object), 200

if __name__ == '__main__':
    app.run()
