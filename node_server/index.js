const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
var cors = require('cors')
const fs = require('fs');

const DB_SERVER = 'mongodb://localhost:27017/northpark';
// const TEST_SERVER = 'mongodb://localhost:27017/testdatabase';
const PORT = 3000;

mongoose.connect(DB_SERVER, { useNewUrlParser: true }, function(err){
    if(err) {console.log("Error!");}
    else {console.log("No error!");}
});

var userSchema = new mongoose.Schema({
    'id': String, 
    'password': String
}, { collection: 'user' });
var userModel = mongoose.model('user', userSchema, 'user');

var dataSchema = new mongoose.Schema({
    'Requestor':Number, 
    'RequestorSeniority':String, 
    'ITOwner':Number, 
    'FiledAgainst':String, 
    'Severity':String, 
    'Priority':String, 
    'daysOpen':Number, 
    'Satisfaction':String, 
    'date':String, 
    'Ticket ID':Number, 
    'Date created':String, 
    'Type':String
}
, { collection: 'data' });
var dataModel = mongoose.model('data', dataSchema, 'data');

// Read from json files
// var questions = mongoose.model('question');

// fs.readFile("jsondata/Sample Data.json", (err, data) => { 
//     if (err) throw err; 
//     console.log(data.toString());

// }) 

// db.collectionName.insertMany(json, function(err,result) {
//     if (err) {
//       // handle error
//     } else {
//       // handle success
//     }
// });
// var mydata = JSON.parse(data);


const app = express();

app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
// Why true above?

app.get("/ping", function(request, response) {
    console.log("GET /ping | "+ JSON.stringify(request.query));
    response.status(200).send({
        message: 'pong'
      })
});

app.post('/login', function(request, response) {
    console.log("POST /login | "+ JSON.stringify(request.body));
    var query  = userModel.where({ id: request.body.username });
    query.findOne(function (err, user) {
        if (err || !user) {
            response.status(401).send({
                'status': 'fail'
            });
        } else if(user.password == request.body.password) {
            response.status(200).send({
                'status': 'success'
            });
        } else {
            response.status(401).send({
                'status': 'fail'
            });
        }
    });
});

app.get("/distinct", function(request, response) {
    var id_list = [];
    console.log("GET /distinct | "+ JSON.stringify(request.query));
    dataModel.distinct(request.query.field, function(err, ids) {
        console.log(ids.sort());
        if (err || !ids) {
            response.status(401).send({
                'status': 'fail'
            });
        } else {
            value_options = [{"text":"Select Value", "value": ""}];
            ids.forEach(function (item, index) {
                value_options.push({"text":item, "value":item});
            });
            response.status(200).send({
                'status': 'success',
                'value_options': value_options
            });
        }
    });
});

app.get("/ticketdata", function(request, response) {
    console.log("GET /ticketdata | "+ JSON.stringify(request.query));
    const numfields = ['Ticket ID', 'Requestor', 'ITOwner', 'daysOpen'];
    if(numfields.includes(request.query.searchSelected) && request.query.searchValue != '') {
        try {
            request.query.searchValue = parseInt(request.query.searchValue);
        }
        catch(err) {
            request.query.searchValue = -1;
        }
    }
    var limit = parseInt(request.query.limit);
    var searchkey = {};
    var sortkey = {'Ticket ID':1};
    var page_skip = (parseInt(request.query.currentPage)-1)*limit;
    if(!(request.query.searchSelected == '' || request.query.searchValue == '')) {
        var searchkey = {};
        searchkey[""+ request.query.searchSelected +""] = request.query.searchValue;
    }
    if(request.query.sortSelected != '' && request.query.sortSelected!='0') {
        var sortkey = {};
        sortkey[""+ request.query.sortSelected +""] = parseInt(request.query.sortOrder);
    }

    dataModel.find(searchkey).sort(sortkey).skip(page_skip).limit(limit).exec(function(err, doc) {
        if (err || !doc) {
            response.status(401).send({
                'status': 'fail'
            });
        } else {
            dataModel.count(searchkey, function(err, count) {
                if(err) {
                    response.status(401).send({
                        'status': 'fail'
                    });
                }
                else {
                    response.status(200).send({
                        'status': 'success',
                        'ticket_data': doc,
                        'total_items': count
                    });
                }
            });
        }  
    });
});

app.delete("/delete/:id", function(request, response){
    console.log("Delete");
    console.log(request.params.id);
    dataModel.deleteOne({"_id":mongoose.Types.ObjectId(request.params.id)}, function(err, data) {
        if (err) {
            response.status(401).send({
                'status': 'fail'
            });
        } else {
            data['status'] = 'success';
            response.status(200).send(data);
        }
    });
});

// Not asynchronous. Required?

// app.post("/person", async (request, response) => {});
// app.get("/people", async (request, response) => {});
// app.get("/person/:id", async (request, response) => {});
// app.put("/person/:id", async (request, response) => {});
// app.delete("/person/:id", async (request, response) => {});

app.listen(PORT, function() {
    console.log(`Server is running on port ${PORT}`);
});





