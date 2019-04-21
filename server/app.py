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

DB_URL = 'mongodb://localhost:27017/'

client = MongoClient(DB_URL)
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

DATA.update_many( {}, { "$rename": { "ticket": "Ticket ID" } } )
DATA.update_many( {}, { "$rename": { "Ticket Creation Date": "Date created" } } )
DATA.update_many( {}, { "$rename": { "TicketType": "Type" } } )

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')

@app.route('/login', methods=['GET', 'POST'])
def login():
    post_data = request.get_json()
    print(post_data)
    result = USER.find_one({'id': post_data.get('username')})
    if not result:
        response_object =  jsonify({'status': 'fail'}), 401
    elif result['password'] == post_data.get('password'):
        response_object = jsonify({'status': 'success'}), 200
    else:
        response_object = jsonify({'status': 'fail'}), 401
    print(response_object)
    return response_object

@app.route('/distinct', methods=['GET'])
def distinct_items():
    result = []
    response_object = {'status': 'success'}
    field = request.args.get('field')
    distinct_items = sorted(DATA.distinct(field))
    result.append({'value':'', 'text':'Select Value'})
    for item in distinct_items:
        result.append({'value':item, 'text':item})
    response_object['value_options'] = result
    return jsonify(response_object)

@app.route('/ticketdata', methods=['GET', 'POST'])
def get_all_data():
    response_object = {'status': 'success'}
    if request.method == 'GET':
        sortSelected, searchSelected, searchValue = \
            request.args.get('sortSelected'), request.args.get('searchSelected'), request.args.get('searchValue')
        if(searchSelected in ['ticket', 'Requestor', 'ITOwner', 'daysOpen'] and searchValue != ''):
            try:
                searchValue = int(searchValue)
            except:
                searchValue = -1
        limit, searchkey = int(request.args.get('limit')), {}
        sortkey = [('ticket',1)]
        page_skip = (int(request.args.get('currentPage'))-1)*limit
        if(not(searchSelected == '' or searchValue == '')):
            searchkey = {searchSelected:searchValue}
        
        if(sortSelected != ''):
            sortkey = [(sortSelected,int(request.args.get('sortOrder')))]

        all_data = list(DATA.find(searchkey).sort(sortkey).skip(page_skip).limit(limit))
        for i in all_data:
            i["_id"] = str(i["_id"])
        response_object['ticket_data'] = all_data
        response_object['total_items'] = DATA.find(searchkey).sort(sortkey).count()
    else:
        post_data = request.get_json()
        new_item = json.loads(post_data)
        new_item["_id"] = ObjectId(new_item["_id"])
        BOOKS.insert_one(new_item)
        response_object['message'] = 'Book added!'
    return jsonify(response_object)


@app.route('/chartdata', methods=['GET'])
def chart_data():
    data_list, label_list = [], []
    response_object = {'status': 'success'}
    item = request.args.get('item')
    for label in sorted(DATA.find().distinct(item)):
        label_list.append(label)
        data_list.append(DATA.find({item:label}).count())
    
    response_object['label_list'] = label_list
    response_object['data_list'] = data_list
    return jsonify(response_object)

@app.route('/delete/<id>', methods=['DELETE'])
def delete_row(id):
    response_object = {'status': 'success'}
    DATA.remove( {"_id": ObjectId(id)})
    response_object['message'] = 'Row removed!'
    return jsonify(response_object)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, threaded=True)
    app.run(host='0.0.0.0')
    # app.run()
