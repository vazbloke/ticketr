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
db = client["northpark"]

collist = db.list_collection_names()
if "books" in collist:
    db.books.drop()
if "data" in collist:
    db.data.drop()
if "user" in collist:
    db.user.drop()

BOOKS = db["books"]
DATA = db["data"]
USER = db["user"]

with open("books.json") as f:
    booksdata = json.load(f)
BOOKS.insert_many(booksdata)

with open("Sample Data.json") as f:
    datadata = json.load(f)
DATA.insert_many(datadata)

with open("User.json") as f:
    userdata = json.load(f)
USER.insert_many(userdata)

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

@app.route('/data', methods=['GET', 'POST'])
def get_all_data():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()

        # don't do this. Just repalce _id and send
        new_item = {
            'Requestor': post_data.get('Requestor'),
            'ITOwner': post_data.get('ITOwner'),
            'read': post_data.get('FiledAgainst'),
            'price': post_data.get('Severity'),
            'Priority': post_data.get('Priority')
        }
        print(new_item)
        BOOKS.insert_one(new_item)
        response_object['message'] = 'Book added!'
    else:
        limit = int(request.args.get('limit'))
        page_skip = int(request.args.get('page'))*limit
        pymongo_cursor = DATA.find().skip(page_skip).limit(limit)
        all_data = list(pymongo_cursor)
        for i in all_data:
            i["_id"] = str(i["_id"])
        response_object['ret_data'] = all_data
    return jsonify(response_object)


@app.route('/login', methods=['GET', 'POST'])
def login():
    post_data = request.get_json()
    print(post_data)
    result = USER.find_one({'id': post_data.get('id')})
    # if not result:
    #     return jsonify({'status': 'fail'}), 401
    if result['password'] == post_data.get('password'):
        return jsonify({'status': 'success'}), 200
    # else:
    #     return jsonify({'status': 'fail'}), 401

if __name__ == '__main__':
    app.run()
