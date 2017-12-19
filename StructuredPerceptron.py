from __future__ import division
import sys,re,random
from collections import defaultdict
from pprint import pprint
import pickle

##########################
# Stuff you will use

from vit_starter import *  # your vit.py from part 1
OUTPUT_VOCAB = set(""" ! # $ & , @ A D E G L M N O P R S T U V X Y Z ^ """.split())

##########################
# Utilities

def dict_subtract(vec1, vec2):
    """treat vec1 and vec2 as dict representations of sparse vectors"""
    out = defaultdict(float)
    out.update(vec1)
    for k in vec2: out[k] -= vec2[k]
    return dict(out)

def dict_argmax(dct):
    """Return the key whose value is largest. In other words: argmax_k dct[k]"""
    return max(dct.iterkeys(), key=lambda k: dct[k])

def dict_dotprod(d1, d2):
    """Return the dot product (aka inner product) of two vectors, where each is
    represented as a dictionary of {index: weight} pairs, where indexes are any
    keys, potentially strings.  If a key does not exist in a dictionary, its
    value is assumed to be zero."""
    smaller = d1 if len(d1)<len(d2) else d2  # BUGFIXED 20151012
    total = 0
    for key in smaller.iterkeys():
        total += d1.get(key,0) * d2.get(key,0)
    return total

def read_tagging_file(filename):
    """Returns list of sentences from a two-column formatted file.
    Each returned sentence is the pair (tokens, tags) where each of those is a
    list of strings.
    """
    sentences = open(filename).read().strip().split("\n\n")
    ret = []
    for sent in sentences:
        lines = sent.split("\n")
        pairs = [L.split("\t") for L in lines]
        tokens = [tok for tok,tag in pairs]
        tags = [tag for tok,tag in pairs]
        ret.append( (tokens,tags) )
    return ret
###############################

## Evaluation utilties you don't have to change

def do_evaluation(examples, weights):
    num_correct,num_total=0,0
    for tokens,goldlabels in examples:
        N = len(tokens); assert N==len(goldlabels)
        predlabels = predict_seq(tokens, weights)
        num_correct += sum(predlabels[t]==goldlabels[t] for t in range(N))
        num_total += N
    print "%d/%d = %.4f accuracy" % (num_correct, num_total, num_correct/num_total)
    return num_correct/num_total

def fancy_eval(examples, weights):
    confusion = defaultdict(float)
    bygold = defaultdict(lambda:{'total':0,'correct':0})
    for tokens,goldlabels in examples:
        predlabels = predict_seq(tokens, weights)
        for pred,gold in zip(predlabels, goldlabels):
            confusion[gold,pred] += 1
            bygold[gold]['correct'] += int(pred==gold)
            bygold[gold]['total'] += 1
    goldaccs = {g: bygold[g]['correct']/bygold[g]['total'] for g in bygold}
    for gold in sorted(goldaccs, key=lambda g: -goldaccs[g]):
        print "gold %s acc %.4f (%d/%d)" % (gold,
                goldaccs[gold],
                bygold[gold]['correct'],bygold[gold]['total'],)

def show_predictions(tokens, goldlabels, predlabels):
    print "%-20s %-4s %-4s" % ("word", "gold", "pred")
    print "%-20s %-4s %-4s" % ("----", "----", "----")
    for w, goldy, predy in zip(tokens, goldlabels, predlabels):
        out = "%-20s %-4s %-4s" % (w,goldy,predy)
        if goldy!=predy:
            out += "  *** Error"
        print out

###############################

## YOUR CODE BELOW


def train(examples, stepsize=1, numpasses=10, do_averaging=False, devdata=None):
    """
    IMPLEMENT ME !
    Train a perceptron. This is similar to the classifier perceptron training code
    but for the structured perceptron. Examples are now pairs of token and label
    sequences. The rest of the function arguments are the same as the arguments to
    the training algorithm for classifier perceptron.
    """

    # features now have format ('c','tag','word'):val for curword and ('tag'):val for biasterm
    weights = defaultdict(float)
    weightsums = defaultdict(float)
    passes = 0

    def get_averaged_weights():
        # IMPLEMENT ME!
        
        averaged_theta = defaultdict(float)
        
        for w in weightsums:
            averaged_theta[w] = weights[w]-(weightsums[w]/passes)
            
        return averaged_theta

    for pass_iteration in range(numpasses):
        print "Training iteration %d" % pass_iteration
        # IMPLEMENT THE INNER LOOP!
        # Like the classifier perceptron, you may have to implement code
        # outside of this loop as well!
        random.shuffle(examples)

        for tokens,goldlabels in examples:
            passes += 1
            predseq = predict_seq(tokens, weights)
            predvec = features_for_seq(tokens, predseq)
            goldvec = features_for_seq(tokens, goldlabels)
            goodness = dict_subtract(goldvec, predvec)
            
            if predseq != goldlabels:
                
                for w in goodness:
                    weights[w] += stepsize*(goodness[w])
                    
                    # update St = St-1+(t-1)rg
                    weightsums[w] += (passes-1)*stepsize*(goodness[w])
          
        # Evaluation at the end of a training iter
        print "TR  RAW EVAL:",
        do_evaluation(examples, weights)
        if devdata:
            print "DEV RAW EVAL:",
            do_evaluation(devdata, weights)
        if devdata and do_averaging:
            print "DEV AVG EVAL:",
            do_evaluation(devdata, get_averaged_weights())
    
    print "Learned weights for %d features from %d examples" % (len(weights), len(examples))

    # NOTE different return value then classperc.py version.
    return weights if not do_averaging else get_averaged_weights()

def predict_seq(tokens, weights):
    """
    IMPLEMENT ME!
    takes tokens and weights, calls viterbi and returns the most likely
    sequence of tags
    """
    
    Ascores, Bscores = calc_factor_scores(tokens, weights)
    seq = viterbi(Ascores, Bscores, OUTPUT_VOCAB)
    
    # once you have Ascores and Bscores, could decode with
    # seq = greedy_decode(Ascores, Bscores, OUTPUT_VOCAB)
    
    return seq

def greedy_decode(Ascores, Bscores, OUTPUT_VOCAB):
    """Left-to-right greedy decoding.  Uses transition feature for prevtag to curtag."""
    N=len(Bscores)
    if N==0: return []
    out = [None]*N
    out[0] = dict_argmax(Bscores[0])
    for t in range(1,N):
        tagscores = {tag: Bscores[t][tag] + Ascores[out[t-1], tag] for tag in OUTPUT_VOCAB}
        besttag = dict_argmax(tagscores)
        out[t] = besttag
    return out

def local_emission_features(t, tag, tokens):
    """
    Feature vector for the B_t(y) function
    t: an integer, index for a particular position
    tag: a hypothesized tag to go at this position
    tokens: the list of strings of all the word tokens in the sentence.
    Retruns a set of features.
    """
    curword = tokens[t]
    feats = {}
    feats["tag=%s_biasterm" % tag] = 1
    feats["tag=%s_curword=%s" % (tag, curword)] = 1
    
    if curword[0] is '#':
        feats["first_char=#_curword=%s" % curword] = 1
    
    if curword[0] is '@':
        feats["first_char=@_curword=%s" % curword] = 1
    
    if '@' in curword and curword[0] is not '@':
        feats["poss_email_curword=%s" % curword] = 1
        
    if curword.istitle():
        feats["capitalized_curword=%s" % curword] = 1
    
    if "'s" in curword:
        feats["poss_possessive_curword=%s" % curword] = 1
    
    return feats

def features_for_seq(tokens, labelseq):
    """
    IMPLEMENT ME!

    tokens: a list of tokens
    labelseq: a list of output labels
    The full f(x,y) function. Returns one big feature vector. This is similar
    to features_for_label in the classifier peceptron except here we aren't
    dealing with classification; instead, we are dealing with an entire
    sequence of output tags.

    This returns a feature vector represented as a dictionary.
    """
    f_vec = defaultdict(float)
    f_vec.update(local_emission_features(0, labelseq[0], tokens))
    
    for w in range(1,len(tokens)):
    
        # add local emission features to vector
        f_vec.update(local_emission_features(w, labelseq[w], tokens))
        
        # add transition features to vector
        f_vec[(labelseq[w-1], labelseq[w])] += 1
        
    return f_vec

def local_emission_features(t, tag, tokens):
    """
    Feature vector for the B_t(y) function
    t: an integer, index for a particular position
    tag: a hypothesized tag to go at this position
    tokens: the list of strings of all the word tokens in the sentence.
    Retruns a set of features.
    """
    curword = tokens[t]
    feats = {}
    feats["tag=%s_biasterm" % tag] = 1
    feats["tag=%s_curword=%s" % (tag, curword)] = 1

    return feats

def calc_factor_scores(tokens, weights):
    """
    IMPLEMENT ME!

    tokens: a list of tokens
    weights: perceptron weights (dict)

    returns a pair of two things:
    Ascores which is a dictionary that maps tag pairs to weights
    Bscores which is a list of dictionaries of tagscores per token
    """
    N = len(tokens)
    # MODIFY THE FOLLOWING LINE

    Ascores = { (tag1,tag2): weights[(tag1,tag2)] for tag1 in OUTPUT_VOCAB
               for tag2 in OUTPUT_VOCAB}
    
    Bscores = []
    for t in range(N):
       
        cur_dict = defaultdict(float)
    
        # gives all output combos per token
        for tag in OUTPUT_VOCAB:
            feat_dict = local_emission_features(t, tag, tokens)
            val = dict_dotprod(feat_dict, weights)
            cur_dict[tag] = val
        
        Bscores.append(cur_dict)
        
    assert len(Bscores) == N
    return Ascores, Bscores

if __name__ == '__main__':
    training_set = read_tagging_file("oct27.train")
    test_set = read_tagging_file("oct27.dev")
    #sol_dict = train(training_set, do_averaging=False, devdata=test_set)
    sol_dict = train(training_set, do_averaging=True, devdata=test_set)
