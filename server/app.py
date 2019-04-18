import requests, json, os

from bson import json_util, ObjectId
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_cors import CORS

from pymongo import MongoClient


DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

# enable CORS
CORS(app)

# client = MongoClient('np-flask', 27017)

print("Connecting to db...")
client = MongoClient('mongodb://localhost:27017/')
db = client["northpark"]

collist = db.list_collection_names()
if "data" in collist:
    db.data.drop()
if "user" in collist:
    db.user.drop()

DATA = db["data"]
USER = db["user"]

with open("jsondata/Sample Data.json") as f:
    datadata = json.load(f)
DATA.insert_many(datadata)

with open("jsondata/User.json") as f:
    userdata = json.load(f)
USER.insert_many(userdata)


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
        sortkey = [('ticket',1)]
        page_skip = (int(request.args.get('currentPage'))-1)*limit
        if(not(searchSelected == '' or searchValue == '')):
            searchkey = {searchSelected:searchValue}
        
        if(sortSelected != ''):
            sortkey = [(sortSelected,int(request.args.get('sortOrder')))]

        all_data = list(DATA.find(searchkey).sort(sortkey))
        # test.skip(page_skip).limit(limit))
        total_items = len(all_data)
        for i in all_data:
            i["_id"] = str(i["_id"])
        response_object['ticket_data'] = all_data[page_skip:page_skip+limit]
        response_object['total_items'] = total_items
    else:
        post_data = request.get_json()
        new_item = json.loads(post_data)
        new_item["_id"] = ObjectId(new_item["_id"])
        BOOKS.insert_one(new_item)
        response_object['message'] = 'Book added!'
    return jsonify(response_object)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, threaded=True)
    app.run()
