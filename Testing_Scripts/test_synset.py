import re
import os
from nltk.corpus import wordnet
import nltk

# Path to the poem files
path = '/home/ian/Documents/Repos/CS-585/E-Dickinson_NLP/edCompleteSimple'
# Get the directory listing of the poem file directory
files = os.listdir(path)
# Concat the path to the directory to the file listing
files = [os.path.join(path, f) for f in files]
# print(files)

# Characters to get rid of
chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\n', '\'', '\'s', '-']

# Get the poems as an array of strings
files_contents = [open(f).read() for f in files]

# List for the poems words as an array of words
poems = []

# Go through all of the poems and replace the chars with an empty string
for content in files_contents:
    temp = content
    for c in chars:
        temp = temp.replace(c, '')
    poems.append(temp)

# Make an array of tuples (word, POS_tag)
pos_tags = []
poems_words = []
for poem in poems:
    # tokenize the poem
    temp2 = nltk.word_tokenize(poem)
    # add the tokenized poem with part of speech tag
    pos_tags.append(nltk.pos_tag(temp2))
    if ''
    # add the word delimited poem to a list
    poems_words.append(re.split('\s+', poem))


# Make an array of poems words and their synonym set
poems_words_synset = []
for poem in poems_words:
    temp = []
    # Make a list of tuples (word, Synset)
    for word in poem:
        temp.append((word, wordnet.synsets(word)))
    # print(temp,'\n\n')
    # Add the list of tuples to the array of poems words
    poems_words_synset.append(temp)


for i, p_words in zip(range(10), poems_words_synset):
    # print(p_words, '\n')
    print('\n', pos_tags[i], '\n')
    for words in p_words:
        print(words)

print('\n')

synsets = []
for i, word_pos in zip(range(10), pos_tags[1]):
    word, pos = word_pos
    syn = word + '.' + str(pos[0].lower()) + '.01'
    synsets.append(syn)

print(synsets)