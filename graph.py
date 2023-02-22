import networkx as nx
from pymongo_get_database import get_database
import json
from flask import Flask, jsonify
from bson.objectid import ObjectId
import itertools
import datetime

import concurrent.futures
from concurrent.futures import as_completed
# app = Flask(__name__)


# @app.route("/Planets", methods = ['GET'])
def getGraphData(id):
    topics = ['tesla', 'apple', 'microsoft', 'nasa', 'amazon', 'BBC', 'cloud', 'fiat'] 


    dbname = get_database()    

    objInstance = ObjectId(id)
    data = []

    for topic in topics :
        try:
            object_cursor = dbname[topic].find({"_id": objInstance})
            for objs in object_cursor:
                articles = json.loads(objs[topic])
                for s in articles.get('articles'):
                    data.append([str(s.get('title')),str(s.get('source')['name']) , str(s.get('author')) , str(objs.get('_id').generation_time)])
        except:
            continue
    
    return data

# print(getGraphData('638b0c7f26b62f04d7bb8d2f')[0])

# G = nx.Graph()
# i = 1
# articles = getGraphData('638b0c7f26b62f04d7bb8d2f')
# sorted(articles,key=lambda x: x[3])

# for data in  articles:
#     G.add_node(data[0])

    # for d in itertools.islice((articles), i, len(articles)):
    #     if data[1] == d[1] or data[2] == d[2]:
    #         G.add_edge(data[0] , d[0])
    #     else :
    #         G.add_edge(data[0],articles[i][0])
    
    # i = i + 1

def get_game_count_last_24_hours(keyword):
    data = {
        "date": {
            "$lt": datetime.datetime.now(),
            "$gt": datetime.datetime.today() - datetime.timedelta(days=200)
        }
    }
    dbname = get_database()
    return len(list(dbname[keyword].find(data)))

records = get_game_count_last_24_hours('fiat')

print(records)








# topics = ['tesla', 'apple', 'microsoft', 'nasa', 'amazon', 'BBC', 'cloud', 'fiat'] 
# graphData = []
# with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
#     futures = [executor.submit(getGraphData, my_data) for my_data in topics ]
#     # iterate over all submitted tasks and get results as they are available
#     for future in as_completed(futures):
#         # get the result for the next completed task
#         result = future.result() # blocks
#         for i in result:
#             graphData.append(i)
#             print(i)




# shutdown the thread pool
#executor.shutdown() # blocks




# if __name__ == '__main__':
#     app.run(host="localhost", port=6993, debug=True)

