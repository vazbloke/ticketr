import os
import uuid
from bson import json_util

# import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS

from flask import Flask, render_template, redirect, url_for, request, jsonify
from pymongo import MongoClient
import requests, json

# Making connection to locally hosted MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.northpark
BOOKS = db.collection
# weather_c = db.weather_c
# map_c = db.map_c


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# BOOKS = [
#     {
#         'id': uuid.uuid4().hex,
#         'title': 'On the Road',
#         'author': 'Jack Kerouac',
#         'read': True,
#         'price': '19.99'
#     },
#     {
#         'id': uuid.uuid4().hex,
#         'title': 'Harry Potter and the Philosopher\'s Stone',
#         'author': 'J. K. Rowling',
#         'read': False,
#         'price': '9.99'
#     },
#     {
#         'id': uuid.uuid4().hex,
#         'title': 'Green Eggs and Ham',
#         'author': 'Dr. Seuss',
#         'read': True,
#         'price': '3.99'
#     }
# ]


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
            'id': uuid.uuid4().hex,
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
        # response_object['books'] = BOOKS
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
        obj = BOOKS.find_one({'id': book_id})
        # for book in BOOKS:
        #     if book['id'] == book_id:
        #         return_book = book
        response_object['book'] = obj
    if request.method == 'PUT':
        post_data = request.get_json()
        BOOKS.delete_one({ "id":book_id})
        new_item = {
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read'),
            'price': post_data.get('price')
        }
        BOOKS.insert_one(new_item)
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        BOOKS.delete_one({ "id":book_id})
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


@app.route('/charge', methods=['POST'])
def create_charge():
#     post_data = request.get_json()
#     amount = round(float(post_data.get('book')['price']) * 100)
#     stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
#     charge = stripe.Charge.create(
#         amount=amount,
#         currency='usd',
#         card=post_data.get('token'),
#         description=post_data.get('book')['title']
#     )
    response_object = {
        'status': 'success',
        'charge': 0
    }
    return jsonify(response_object), 200


@app.route('/charge/<charge_id>')
def get_charge(charge_id):
    # stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
    response_object = {
        'status': 'success',
        'charge': 0
    }
    return jsonify(response_object), 200

if __name__ == '__main__':
    app.run()
