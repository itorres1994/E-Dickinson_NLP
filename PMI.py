from __future__ import division
import sys,json,math
import os
import numpy as np
from collections import defaultdict

def prepare(poslist, neglist, filename):
    
    # Takes a filename, positive wordlist, and negative wordlist
    # Removes @, #, and URLs from tweets and converts
    # poswords to POS_WORD and negwords to NEG_WORD.
    # Returns list of list representation of tweets
    
    prepped = []
    
    with open(filename,"r") as f_in:
        for line in f_in:
            line = line.split()
            line = [x.lower() for x in line]
            tweet = []
            for word in line:
                if word[0] != '@' and word[0] != '#':
                    tweet.append(word)
            tweet = ['POS_WORD' if x in poslist else x.lower() for x in tweet]
            tweet = ['NEG_WORD' if x in neglist else x for x in tweet]
            prepped.append(tweet)
    
    return prepped
                
def getCounts(tweets):
    
    # Takes list of list representation of tweets, returns defaultdict
    # with {word: tweet count}. Also includes counts of tuples of each word
    # with POS_WORD and NEG_WORD.
    
    counts = defaultdict(float)
    
    for tweet in tweets:
        tweet = set(tweet)
        
        for word in tweet:
            if word != "POS_WORD" and word != "NEG_WORD" and word[:4] != "http":
                if "POS_WORD" in tweet:
                    counts[(word, "POS_WORD")] += 1
                if "NEG_WORD" in tweet:
                    counts[(word, "NEG_WORD")] += 1
            
            counts[word] += 1
        
    return counts
   
def calcPMI(counts, csize):
    
    # Takes dict of counts and size of corpus, returns dict of PMIs for all words
    # in counts. Uses Laplace smoothing for zeroes.
    
    k = .75
    pmis = defaultdict(float)
    ppos = counts["POS_WORD"]/csize
    pneg = counts["NEG_WORD"]/csize
    
    for word in counts.keys():
        
        if type(word) is not tuple:
            
            jointpos = counts[(word, "POS_WORD")]+k/csize
            jointneg = counts[(word, "NEG_WORD")]+k/csize
            pword = counts[word]+k/csize
          
            pmis[(word, "POS_WORD")] = math.log(jointpos/(pword*ppos))
            pmis[(word, "NEG_WORD")] = math.log(jointneg/(pword*pneg))
    
    return pmis

def turney(pmis, word):
    
    # Takes dict of PMIs and returns polarity according to the Turney method.
    
    return pmis[(word, "POS_WORD")]-pmis[(word, "NEG_WORD")]
    
    
    