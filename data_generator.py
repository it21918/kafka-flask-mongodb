import json
import requests
from datetime import date
from bson.objectid import ObjectId
import itertools 
import datetime
import networkx as nx
from pymongo_get_database import get_database

#get articles
def get_articles(topic) :

    date_today = date.today()

    #y/mm/dd
    date_today = date_today.strftime("%y-%m-%d")

    url = "https://newsapi.org/v2/top-headlines?q=" + topic + "&from=" + date_today + "&sortBy=publishedAt&apiKey=a7a6905553244317a359d0f330d3b3e2"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)

#get description of source domain names
def domain_names_description(json_file):
    wiki = []

    if json_file is not None:
        for s in json_file.get('articles'):
            wiki.append(mediaWiki(s.get('source')['name']))

    return  wiki

def mediaWiki(source):
    url = "https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exsentences=10&exlimit=1&titles=" + source + "&explaintext=1&formatversion=2&format=json"

    payload = {}
    headers = {
        'Cookie': 'GeoIP=US:VA:Ashburn:39.05:-77.49:v4; WMF-Last-Access-Global=15-Nov-2022; WMF-Last-Access=15-Nov-2022; enwikiBlockID=14675105%21c32a1f79e2c70302b86474755e78359e47dec74eee8732be91eac3225a047ac43e4369487c6c8b10d8bdda45c8aaeb72bb61b8617327897e5d3af54b54c8e37f'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    for d in json.loads(response.text)['query'].get('pages'): 
        try:
            return {"title" : d['title'] , "description": d['extract']}
        except KeyError:
            return 

def getGraphData():
    topics = ['tesla', 'apple', 'microsoft', 'nasa', 'amazon', 'BBC', 'cloud', 'fiat'] 
    dbname = get_database()    
    articles = []
    G = nx.Graph()

    for topic in topics :
        articlesCursor = dbname[topic].find()

        for article in articlesCursor:

            article = json.loads(json.dumps(article, default=str))
            articles.append([str(article['_id']), str(article['article']['publishedAt']), str(article['article']['source']['name']) , str(article['article']['author'])])
            G.add_node(str(article['_id']))

    sorted(articles,key=lambda x: x[1])
    return G, articles

def createGraph():
    i = 1
    G, articles = getGraphData()

    for article in articles:
        for data in itertools.islice((articles), i, len(articles)):
            if data[2] == article[2]:
                G.add_edge(data[0], article[0])
            elif data[3] == article[3]:
                G.add_edge(data[0], article[0])
            else:
                G.add_edge(article[0], articles[i][0])
        i = i + 1

    nx.write_gml(G, "graphFile.py")
    return G
