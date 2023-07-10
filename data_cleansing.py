import re
import pandas as pd

df = pd.read_csv(
    "/Users/pro2015/Desktop/chapter 3 binar/data/challenge gold/app.py/data.csv", encoding="latin-1")
new_kamusalay = pd.read_csv(
    "/Users/pro2015/Desktop/chapter 3 binar/data/challenge gold/app.py/new_kamusalay.csv", encoding="latin-1")
abusive = pd.read_csv(
    "/Users/pro2015/Desktop/chapter 3 binar/data/challenge gold/app.py/abusive.csv", encoding="latin-1")

list_of_abusive_word = abusive['ABUSIVE'].tolist()
new_kamus_alay = {}
for k, v in new_kamusalay.values:
    new_kamus_alay[k] = v


def processing_word(input_tweets):
    new_tweets = []
    new_new_tweets = []
    tweets = input_tweets.split(" ")
    for word in tweets:
        if word in list_of_abusive_word:
            continue
        else:
            new_tweets.append(word)
    for word in new_tweets:
        new_word = new_kamus_alay.get(word, word)
        new_new_tweets.append(new_word)

    tweets = " ".join(new_new_tweets)
    return tweets


def processing_text(tweets):

    tweets = re.sub(r'\\[0-9A-z]{2,}', ' ', str(tweets))
    tweets = re.sub(
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', 'EMAIL', tweets)
    tweets = tweets.lower()
    tweets = re.sub(r'[^\w\s]', '', tweets)
    tweets = re.sub(r"\b\d{4}\s?\d{4}\s?\d{4}\b", "NOMOR_TELEPON", tweets)
    tweets = tweets.replace(" 62", " 0")
    tweets = tweets.replace("USER", "")
    tweets = tweets.strip()
    tweets = processing_word(tweets)

    return tweets
