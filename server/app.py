import os
from bson import json_util, ObjectId

# import stripe
from flask import Flask, jsonify, request
from flask_cors import CORS

from flask import Flask, render_template, redirect, url_for, request, jsonify
from pymongo import MongoClient
import requests, json

HOST = os.environ['DB_HOST']
# HOST = 'mongodb://localhost:27017/'

DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# client = MongoClient('np-flask', 27017)
client = MongoClient('mongodb://np-mongodb:27017/')
db = client["northpark"]

DATA = db["data"]
USER = db["user"]


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

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

@app.route('/ticketdata', methods=['GET', 'POST'])
def get_all_data():
    response_object = {'status': 'success'}
    if request.method == 'GET':
        sortSelected, searchSelected, searchValue = \
            request.args.get('sortSelected'), request.args.get('searchSelected'), request.args.get('searchValue')
        limit, searchkey = int(request.args.get('limit')), {}
        page_skip = int(request.args.get('currentPage'))*limit
        if(not(searchSelected == '' or searchValue == '')):
            searchkey = {searchSelected:searchValue}
        
        if(sortSelected != ''):
            sortkey = [(sortSelected,int(request.args.get('sortOrder')))]
            pymongo_cursor = DATA.find(searchkey).sort(sortkey).skip(page_skip).limit(limit)
        else:
            pymongo_cursor = DATA.find(searchkey).skip(page_skip).limit(limit)

        all_data = list(pymongo_cursor)
        for i in all_data:
            i["_id"] = str(i["_id"])
        response_object['ticket_data'] = all_data
    else:
        post_data = request.get_json()
        new_item = json.loads(post_data)
        new_item["_id"] = ObjectId(new_item["_id"])
        BOOKS.insert_one(new_item)
        response_object['message'] = 'Book added!'
    return jsonify(response_object)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
