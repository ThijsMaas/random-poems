#!/usr/bin/python3
""" 
utils for script here
"""
import re

def countsyllable(word):
    """Return the amount of syllables in a word (int)

    Args:
    word, string - a word

    
    """
    word = str(word).lower()
    # words 3 or smaller count as 1:
    if len(word) < 4:
        return 1
    # each vowel is a syllable:
    regex = r"[aeiouy]{1,2}"
    count = len(re.findall(regex, word))
    # words that end with -es -ed -e get -1
    for suffix in ('es', 'ed', 'e'):
        if word.endswith(suffix):
            count -= 1
            break
    if count == 0:
        count += 1 
    return count