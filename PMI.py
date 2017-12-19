from __future__ import division
import sys,json,math
import os
import numpy as np
from collections import defaultdict

def prepare(poslist, neglist, dirname):
    
    # Takes a filename, positive wordlist, and negative wordlist
    # Removes @, #, and URLs from tweets and converts
    # poswords to POS_WORD and negwords to NEG_WORD.
    # Returns list of list representation of poems
    
    prepped = []

    for file in os.listdir(dirname):
        
        with open(dirname+"/"+file, 'r') as in_file:
            
            poem = in_file.read().split()
            poem = [x.lower() for x in poem]

            for word in poem:    # ignore poem number
                poem = ['POS_WORD' if x in poslist else x for x in poem]
                poem = ['NEG_WORD' if x in neglist else x for x in poem]

            prepped.append(poem)

    return prepped
                
def getCounts(poems):
    
    # Takes list of list representation of poems, returns defaultdict
    # with {word: poems count}. Also includes counts of tuples of each word
    # with POS_WORD and NEG_WORD.
    
    counts = defaultdict(float)
    
    for poem in poems:
        poem = set(poem[1:])
        
        for word in poem:
            if word != "POS_WORD" and word != "NEG_WORD":
                
                if "POS_WORD" in poem:
                    counts[(word, "POS_WORD")] += 1
                if "NEG_WORD" in poem:
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
    
    for word in list(counts.keys()):
        
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
    
    
    