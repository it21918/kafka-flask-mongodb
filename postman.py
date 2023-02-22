from flask import Flask, jsonify
import time
from pymongo_get_database import get_database
from flask import request
from pymongo import MongoClient
from bson.json_util import dumps
import json
from bson import ObjectId
import threading
from collections import defaultdict
import networkx as nx
from data_generator import translate_text,find_article_byId
from tw_sentiment import analysis
import requests
import json
from tw_sentiment import analysis

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

#Get recommended article id
@app.route("/<string:id>/<string:target>", methods = ['GET'])
def getNeighborBiggestDeggree(id, target):
    G = nx.read_gml("graphFile.py")
    
    try:
        neighbors = nx.neighbors(G, id)
        maxDegreeNeighbor = max(G.degree(list(neighbors)))
        article = find_article_byId(maxDegreeNeighbor[0])
        translated_Article = translate_text(str(article), target)

        return "Recommended Article Translated in "+target+": "+translated_Article
    except Exception as e:
        return dumps({'error' : str(e)})

@app.route('/get/tweets/<string:name>', methods=["GET"])
def get_tweets(name):
    dbname = get_database()  
    try :
        tweets = dbname["tweets"].find_one({"author": name}, {"tweets" : 1})
        tweets = json.loads(json.dumps(tweets, default=str))
        tweets_sentiment = analysis(tweets['tweets'])
        new_line = '\n'
        result = f"{tweets} {new_line} Sentiment analysys: {tweets_sentiment}"
        return result
    except Exception as e:
        return dumps({'error' : str(e)})    

@app.route('/get/<string:email>', methods=["GET"])
def get_data(email):
    dbname = get_database()  
    res = defaultdict(list)

    user = dbname["users"].find_one({"email": email}, {"keywords" : 1})
    for keyword in user['keywords']:
        object_cursor = dbname[keyword].find()

        for objs in object_cursor:
            article = json.loads(json.dumps(objs, default=str))

            source_domain = dbname['domain_name_description'].find_one({'title' : article['article']['source']['name']}, {'description' : 1})
            if source_domain is not ('' or None):
                key = "Article "+ keyword + ": " + str(article['article']) + "  source domains description:" + str(source_domain['description'])
                dictionary = {key : article['article']['source']['name']}
                for key, val in sorted(dictionary.items()):
                    res[val].append(key)            
            else :
                key = "Article "+ keyword + ": " + str(article['article']) + "  source domains description: None"
                dictionary = {key : article['article']['source']['name']}
                for key, val in sorted(dictionary.items()):
                    res[val].append(key)   

    return ("Grouped dictionary is : " + str(dict(res)))

@app.route('/update/<string:email>', methods = ['PUT'])
def update_data(email):
    dbname = get_database()    
    try:
        data = json.loads(request.data)
        keywords = data['keywords']
        status = dbname["users"].update_one({"email":email},{"$set": {"keywords":keywords}})
        print(status)
        return dumps({'message' : 'SUCCESS'})
    except Exception as e:
        return dumps({'error' : str(e)})        

# POST API
@app.route('/add', methods = ['POST'])
def post_data():
    dbname = get_database()    

    try:
        data = json.loads(request.data)
        user_email = data['email']
        user_country = data['country']
        user_city = data['city']
        keywords = data['keywords']
        if user_email:
            #status = collection_name.insert_one({"email" : user_email,"city" : user_city,"timestamp" : time.time(),"keywords" : keywords})
            status = dbname["users"].replace_one(
                {"email" : user_email},
                {"email": user_email,'country' : user_country, "city" : user_city,"timestamp" : time.time(),"keywords" : keywords},  upsert=True)
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
    app.run(host="localhost", port=7000, debug=True)
