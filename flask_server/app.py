import requests, json, os

from bson import json_util, ObjectId
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from datetime import datetime

from db_functions import import_data, initialize_db

DB_SERVER = 'mongodb://localhost:27017/'
DB_NAME = "northpark"

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
CORS(app)

# setup mongo
mongo_client = MongoClient(DB_SERVER)
db = mongo_client[DB_NAME]
initialize_db(db)

# import data into data and user collections
DATA = db["data"]
USER = db["user"]
import_data(USER, DATA)

@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong')

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

@app.route('/ticketdata', methods=['GET'])
def get_all_data():
    response_object = {'status': 'success'}
    sortSelected, searchSelected, searchValue = \
        request.args.get('sortSelected'), request.args.get('searchSelected'), request.args.get('searchValue')
    if(searchSelected in ['Ticket ID', 'Requestor', 'ITOwner', 'daysOpen'] and searchValue != ''):
        try:
            searchValue = int(searchValue)
        except:
            searchValue = -1
    limit, searchkey = int(request.args.get('limit')), {}
    sortkey = [('Ticket ID',1)]
    page_skip = (int(request.args.get('currentPage'))-1)*limit
    if(not(searchSelected == '' or searchValue == '')):
        searchkey = {searchSelected:searchValue}
    
    if(sortSelected != '' and sortSelected!='0'):
        sortkey = [(sortSelected,int(request.args.get('sortOrder')))]

    all_data = list(DATA.find(searchkey).sort(sortkey).skip(page_skip).limit(limit))
    for i in all_data:
        i["_id"] = str(i["_id"])
    response_object['ticket_data'] = all_data
    response_object['total_items'] = DATA.find(searchkey).sort(sortkey).count()
    return jsonify(response_object)


@app.route('/singlechart', methods=['GET'])
def single_chart():
    data_list, label_list = [], []
    response_object = {'status': 'success'}
    robject = {}
    item = request.args.get('item')
    print(item)
    for label in sorted(DATA.find().distinct(item)):
        label_list.append(label)
        data_list.append(DATA.find({item:label}).count())
    datasets = []
    temp_obj = {}
    temp_obj['data'] = data_list

    temp_obj['label'] = item

    if(item == 'Satisfaction'):
        temp_obj['backgroundColor'] = ["#FF9F40", "#FFCD56","#FF6383","#4BC0C0","#36A2EB"]
    elif(item == 'Priority'):
        temp_obj['backgroundColor'] = ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"]
    else:
        temp_obj['backgroundColor'] = ["#E46651", "#41B883", "#00D8FF", "#33B5E5"]
    robject['labels'] = label_list
    datasets.append(temp_obj)
    robject['datasets'] = datasets
    response_object['chart_data'] = robject
    return jsonify(response_object)

@app.route('/dualchart', methods=['GET'])
def dual_chart():
    data_list, label_list = [], []
    response_object = {'status': 'success'}
    robject = {}
    item = request.args.get('item')
    cat_by = request.args.get('cat_by')
    print(item)
    datasets = []
    colorlist = ["#9966FE", "#FFCD56", "#41B883", "#E46651", "#00D8FF", "#33B5E5"]
    for i, cat in enumerate(sorted(DATA.find({}).distinct(cat_by))):
        label_list, data_list = [], []
        temp_obj = {}
        for label in sorted(DATA.find({cat_by:cat}).distinct(item)):
            label_list.append(label)
            data_list.append(DATA.find({cat_by:cat, item:label}).count())
        temp_obj['data'] = data_list
        temp_obj['backgroundColor'] = colorlist[i]
        temp_obj['label'] = cat
        datasets.append(temp_obj)
    robject['labels'] = label_list
    robject['datasets'] = datasets
    response_object['chart_data'] = robject
    return jsonify(response_object)

@app.route('/linechart', methods=['GET'])
def line_chart():
    data_list, label_list = [], []
    response_object = {'status': 'success'}
    item = request.args.get('item')
    for label in sorted(DATA.find().distinct(item)):
        label_list.append(label)
        data_list.append(DATA.find({item:label}).count())
    robject, tmp_obj = {}, {}
    robject['labels'] = label_list
    datasets = []
    tmp_obj['label'] = item
    tmp_obj['backgroundColor'] = '#FF6383'
    tmp_obj['pointBackgroundColor'] = '#FC2525'
    tmp_obj['data'] = data_list
    datasets.append(tmp_obj)
    robject['datasets'] = datasets
    response_object['chart_data'] = robject
    return jsonify(response_object)

@app.route('/delete/<id>', methods=['DELETE'])
def delete_row(id):
    response_object = {'status': 'success'}
    DATA.remove( {"_id": ObjectId(id)})
    response_object['message'] = 'Row removed!'
    return jsonify(response_object)

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
    # Enable line below for Docker 
    # app.run(host='0.0.0.0', port=5000, threaded=True)

