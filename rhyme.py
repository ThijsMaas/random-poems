#!/usr/bin/python3
""" 
feed sentences into this script until a rhyme comes out
"""

from nltk.corpus import cmudict

class Arpabet():
    def __init__(self):
        self.arpabet = cmudict.dict()
        self.entries = self.arpabet.keys()

    def get(self, word):
        """Return arpabet of a word as a tuple"""
        try:
            return self.arpabet[word][0]
        except KeyError:
            entry = self.findEntry(word)
            if entry:
                return self.arpabet[entry][0]

    def findEntry(self, word):
        """Returns an entry with the same suffix"""
        for i in range(3,10):
            if word[-i:] in self.entries:
                return word[-i:]
            else:
                return False
    
    def accent(self, arpabet):
        """return the last accented last syllable of a list of arpabet characters"""
        for i, letter in enumerate(arpabet[::-1]):
            if letter.endswith(('1','2','3')):
                return arpabet[-i-1:]

def main():
    arpabet = Arpabet()
    word = arpabet.get('create')
    print(word)
    print(arpabet.accent(word))

if __name__ == '__main__':
    main()
