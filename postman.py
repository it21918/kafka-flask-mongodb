from flask import Flask
import time
from pymongo_get_database import get_database
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
import json

app = Flask(__name__)

# POST API
@app.route('/add', methods = ['POST'])
def post_data():
    dbname = get_database()    
    collection_name = dbname["users"]

    try:
        data = json.loads(request.data)
        user_email = data['email']
        if user_name and user_contact:
            status = collection_name.insert_one({
                "email" : user_email
            })
        print(status)
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})
        





if __name__ == '__main__':
    app.run()