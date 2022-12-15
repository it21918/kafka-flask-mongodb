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

def to_representation(value):
    try:
        result = json.dumps(value, skipkeys=True, allow_nan=True,cls=JSONEncoder)
        return result
    except ValueError:
        return ''


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


# def get_dom(articles_cursor):
#     for article in articles_cursor['articles']:
#         print(article.get('source')['name'])

# def get_articles(keyword):
#     dbname = get_database()
#     print(keyword)
#     return dbname[keyword].collection_name.find()

#get
@app.route('/get/<string:email>', methods=["GET"])
def get_data(email):
    dbname = get_database()    

    user = dbname["users"].find_one({"email": email}, {"keywords" : 1})
    for keyword in user['keywords']:
        print(keyword)
        articles_cursor = dbname[keyword].find()
        #articles_cursor = articles_cursor.toArray()
        #print(articles_cursor[0])

        # t1 = threading.Thread(target=get_articles, args=keyword)
        # t2 = threading.Thread(target=get_dom, args=get_articles(keyword))
 
        # t1.start()
        # t2.start()
        # t1.join()
        # t2.join()


    # for article in articles_cursor['articles']:
    #     print(article.get('source')['name'])

    return ''

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
    app.run(host="localhost", port=7600, debug=True)
