from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from data_generator import translate_text

from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
from data_generator import translate_text

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
import re

def preprocess(tweet):
    # Replace usernames with "@user"
    tweet = re.sub(r'@\S+', '@user', tweet)
    # Replace URLs with "http"
    tweet = re.sub(r'http\S+', 'http', tweet)
    # Remove stop words
    stop_words = set(stopwords.words('english'))
    tweet_words = [word for word in tweet.split() if word.lower() not in stop_words]
    # Remove punctuation and special characters
    tweet_words = [re.sub(r'[^\w\s]','', word) for word in tweet_words]
    # Join words back into string
    tweet_proc = " ".join(tweet_words)
    return tweet_proc

def analysis(tweet):
    # Preprocess tweet
    tweet_proc = preprocess(tweet)

    # Load model and tokenizer
    roberta = "cardiffnlp/twitter-roberta-base-sentiment"
    model = AutoModelForSequenceClassification.from_pretrained(roberta)
    tokenizer = AutoTokenizer.from_pretrained(roberta)

    # Define labels
    labels = ['Negative', 'Neutral', 'Positive']

    # Translate tweet to English
    tweet_proc = translate_text(tweet_proc, 'en')

    # Perform sentiment analysis
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    output = model(**encoded_tweet)

    # Convert output to probabilities
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)
    
    result = ''
    for i in range(len(scores)):
        result = str(labels[i]) + ' ' + str(scores[i]) + '\n' + result

    return result