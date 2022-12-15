from flask import Flask
import time
from pymongo_get_database import get_database
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
import json

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

# POST API
@app.route('/add', methods = ['POST'])
def post_data():
    dbname = get_database()    
    collection_name = dbname["users"]

    try:
        data = json.loads(request.data)
        user_email = data['email']
        if user_email:
            status = collection_name.insert_one({
                "email" : user_email
            })
        print(status)
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})
        





if __name__ == '__main__':
    app.run()
