import json
import requests
from datetime import date

#get articles
def get_articles(topic) :

    today = date.today()

    #y/mm/dd
    date_y_mm_dd = today.strftime("%y-%m-%d")

    url = "https://newsapi.org/v2/everything?q=" + topic + "&from=" + date_y_mm_dd + "&sortBy=publishedAt&apiKey=a7a6905553244317a359d0f330d3b3e2"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text

#get description of source domain names
def domain_names_description(jsonFile):
    j = json.loads(jsonFile)
    wiki = []

    if j is not None:
        for s in j.get('articles'):
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
            return (d['extract'])  
        except KeyError:
            return 
