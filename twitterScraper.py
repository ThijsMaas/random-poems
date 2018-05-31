#!/usr/bin/python3
""" 
This script makes the poems from the sentences
"""

import re
import json
import tweepy
from utils import countsyllable

class Listener(tweepy.StreamListener):
    """StreamListener"""
    def __init__(self, api=None):
        self.api = api
        self.counter = 0
        self.data = []

    def on_status(self, tweet):
        
        if self.counter >= 100:
            return False
        else:
            tweet = filter(tweet.text)
            if tweet:
                self.counter += 1
                self.data.append(tweet)
                
    def on_error(self, tweet):
        print(tweet.text)
        exit()
    

def getTokens(keyfile):
    d = {}
    with open (keyfile) as f:
        for line in f.readlines():
            key, value = line.strip().split('\t')
            d[key] = value
    return d

def filter(tweet):
    # emoticons_str = r"""
    #     (?:
    #         [:=;] # Eyes
    #         [oO\-]? # Nose (optional)
    #         [D\)\]\(\]/\\OpP] # Mouth
    #     )"""
 
    # regex_str = [
    #     emoticons_str,
    #     r'<[^>]+>', # HTML tags
    #     r'(?:@[\w_]+)', # @-mentions
    #     r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    #     r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs
    
    #     r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    #     r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    #     r'(?:[\w_]+)', # other words
    #     r'(?:\S)' # anything else
    # ]
    
    # tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
    # emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)
 
    tweetlow = tweet.lower()
    # remove retweets
    retweets = ['@', 'rt', '.']
    for rt in retweets:
        if tweetlow.startswith(rt):
            return None
    # remove links
    if 'www' in tweetlow or 'http' in tweetlow or '.com' in tweetlow:
        return None
    # clean the text
    tweet = cleantext(tweet)
    # take reasonable sized tweets
    total_syllable = sum(countsyllable(word) for word in tweet.split(' '))
    if not 5 <= total_syllable <= 16:
        return None
    return tweet

def cleantext(text):
    text = text.strip()
    replace_dict = {
        '&':'and', 
    }
    # replace html entities
    
    # remove text smileys
    smileys = [":s", ":p", ":d", ":x", "xd", ":o(", ":o)", ":-s", ":-d", 
               ":-p", ":-x", ";d", ":3", "<3", '</3', "T_T"]
    for smiley in smileys:
        text = text.replace(smiley, '')
    # remove everything but words, digits and whitespace
    text = ''.join(re.findall(r"[a-zA-Z\d\s'.,:]", text))

    # translate number into words

    return text
    
def fetch(tags=None, languages=None):
    tags = ['and', 'the', 'am', 'i', 'is', 'to'] 
    keys = getTokens('twitter.keys')
    auth = tweepy.OAuthHandler(keys['consumer_key'], keys['consumer_secret'])
    auth.set_access_token(keys['access_token_key'], keys['access_token_secret'])
    
    api = tweepy.API(auth)
    listener = Listener(api)
    twitterStream = tweepy.Stream(auth, listener)
    try:
        twitterStream.filter(track=tags, languages=['en'])
    except:
        print('Error')
        twitterStream.disconnect()
        exit()
    for tweet in listener.data:
        yield tweet

def main():
    for tweet in fetch():
        tweet = filter(tweet)
        if tweet:
            print(tweet)
if __name__ == '__main__':
    main()