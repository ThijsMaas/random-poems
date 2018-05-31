#!/usr/bin/python3
""" 
Main
"""

from twitterScraper import fetch
from utils import countsyllable

def main():
    for tweet in fetch():
        print(tweet)

if __name__ == '__main__':
    main()