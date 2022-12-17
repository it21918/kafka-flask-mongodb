from flask import Flask, jsonify
import time
from pymongo_get_database import get_database
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
import json
from bson import ObjectId
from serializers import JSONEncoder
import threading
from collections import defaultdict

app = Flask(__name__)

# Endpoint for deleting user
@app.route("/delete/<email>", methods=["DELETE"])
def guide_delete(email):
    dbname = get_database()    
    collection_name = dbname["users"]

    myquery = { "email": email }
    try:
        collection_name.delete_one(myquery)
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})


def split(a_list):
    half = len(list(a_list))//2
    return a_list[:half], a_list[half:]

#get
@app.route('/get/<string:email>', methods=["GET"])
def get_data(email):
    dbname = get_database()    

    user = dbname["users"].find_one({"email": email}, {"keywords" : 1})
    for keyword in user['keywords']:
        object_cursor = dbname[keyword].find()

        for objs in object_cursor:
            articles = json.loads(objs[keyword])
            for s in articles.get('articles'):
                source_domain = dbname['domain_name_description'].find_one({'title' : s.get('source')['name']}, {'description' : 1})
                if source_domain is not ('' or None):
                    key = "Article:" + str(s) + "  source domains description:" + str(s['description'])
                    dictionary = {key : s.get('source')['name']}
                else :
                    key = "Article:" + str(s) + "  source domains description: None"
                    dictionary = {key : s.get('source')['name']}
                    
        break
    res = defaultdict(list)
    for key, val in sorted(dictionary.items()):
        res[val].append(key)
    return ("Grouped dictionary is : " + str(dict(res)))
        

# POST API
@app.route('/add', methods = ['POST'])
def post_data():
    dbname = get_database()    
    collection_name = dbname["users"]

    try:
        data = json.loads(request.data)
        user_email = data['email']
        user_city = data['city']
        keywords = data['keywords']
        if user_email:
            status = collection_name.insert_one({
                "email" : user_email,
                "city" : user_city,
                "timestamp" : time.time(),
                "keywords" : keywords

            })
        print(status)
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})
        
#for testing  JSON raw POST
    # {
    #     "email": "it21918@hua.gr",
    #     "city": "Athens",
    #     "keywords": ["apple", "tesla"]

    # }


if __name__ == '__main__':
    app.run(host="localhost", port=6993, debug=True)
