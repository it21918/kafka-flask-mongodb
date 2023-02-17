import json
import requests
from datetime import date
from bson.objectid import ObjectId
import itertools
import datetime
from pymongo_get_database import get_database
from tweets import get_tweets
import detectlanguage


api_key = "3c37eebc6emsh35f362a88575178p178e44jsnf1217afebe34"
detectlanguage.configuration.api_key = "cbd4f69ae68cfcb38ddf0dd115caa1ef"


def translate(target):
    dbname = get_database()
    topics = ['tesla', 'apple', 'microsoft',
              'nasa', 'amazon', 'BBC', 'cloud', 'fiat']
    for topic in topics:
        article = dbname[topic].find_one(
            {'_id': ObjectId('63c427ae0192e94191816bcb')})
        if article is not None:
            break


    json_article = json.dumps(article['article']['title'])
    json_article = json.loads(json_article)
    #print(str(json_article))
    translate_text(str(json_article), target, api_key)


def translate_text(text, target_lang, api_key):

    source_lang = detectlanguage.simple_detect(text)

    url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

    payload = f"q={text}&target={target_lang}&source={source_lang}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "google-translate1.p.rapidapi.com",
        "Accept-Encoding": "application/gzip"
    }

    response = requests.request("POST", url, data=payload, headers=headers)
    response = json.loads(response.text)
    print(response['data']['translations'][0]['translatedText'])
    return response['data']['translations'][0]['translatedText']
