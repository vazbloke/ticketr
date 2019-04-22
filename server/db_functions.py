import pymongo, json
from datetime import datetime

def initialize_db(db):
    collection_list = db.list_collection_names()
    if "data" in collection_list:
        db.data.drop()
    if "user" in collection_list:
        db.user.drop()

def import_data(user_collection, data_collection):
    with open("jsondata/Sample Data.json") as f:
        datadata = json.load(f)

    print("Reading user data...")
    with open("jsondata/User.json") as f:
        userdata = json.load(f)
    user_collection.insert_many(userdata)

    records = []
    print("Reading ticket data...")
    for entry in datadata:
        if entry['Ticket Creation Date']:
            date = datetime.strptime(entry['Ticket Creation Date'], "%m/%d/%Y")
            date = date.isoformat()
            entry['date'] = date
        entry["Ticket ID"] = entry["ticket"]
        entry["Date created"] = entry["Ticket Creation Date"]
        entry["Type"] = entry["TicketType"]
        entry.pop('ticket', None)
        entry.pop('Ticket Creation Date', None)
        entry.pop('TicketType', None)
        records.append(entry)

    data_collection.insert_many(records)