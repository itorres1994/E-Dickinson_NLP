import re
import os
import json
from nltk.corpus import wordnet
import nltk
from tqdm import tqdm


def initialize_files():
    # Path to the poem files
    path = '/home/ian/Documents/Repos/CS-585/E-Dickinson_NLP/edCompleteSimple'
    # Get the directory listing of the poem file directory
    files = os.listdir(path)
    # Concat the path to the directory to the file listing
    files = [os.path.join(path, f) for f in tqdm(files,'set file paths')]
    # print(files)
    return files


# Get the poem files listing
files = initialize_files()


def clean_words_in_poems():
    # Characters to get rid of
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '\n', '\'', '\'s', '-']

    # Get the poems as an array of strings
    files_contents = [open(f).read() for f in tqdm(files, 'read poems')]

    # List for the poems words as an array of words
    poems = []

    # Go through all of the poems and replace the chars with an empty string
    for content in tqdm(files_contents, 'spring cleaning'):
        temp = content
        for c in chars:
            temp = temp.replace(c, '')
        if temp is not '':
            poems.append(temp)
    return poems


# Get the contents of all poems
poems = clean_words_in_poems()


def pos_tagging():
    # Make an array of tuples (word, POS_tag)
    pos_tags = []
    poems_words = []
    for poem in tqdm(poems, 'tagging words in poem'):
        # tokenize the poem
        temp2 = nltk.word_tokenize(poem)
        # add the tokenized poem with part of speech tag
        pos_tags.append(nltk.pos_tag(temp2))
        # add the word delimited poem to a list
        poems_words.append(re.split('\s+', poem))
    return pos_tags, poems_words


# Get the poems contents delimited by spaces and their pos_tags
pos_tags, poems_words = pos_tagging()


# def exp_pos_tagging():
#     alt_pos_tags = []
#     for poem in poems_words:
#         # print(poem)
#         temp = []
#         for word in poem:
#             if word is not '':
#                 # print(word, ',', nltk.pos_tag([word]))
#                 temp.append(nltk.pos_tag([word])[0])
#         alt_pos_tags.append(temp)
#     return alt_pos_tags
#
#
# alt_pos_tags = exp_pos_tagging()


def get_synsets():
    # Make an array of poems words and their synonym set
    poems_words_synset = []
    for poem in tqdm(poems_words, 'loading synsets current build'):
        temp = []
        # Make a list of tuples (word, Synset)
        for word in poem:
            temp.append((word, wordnet.synsets(word)))
        # print(temp,'\n\n')
        # Add the list of tuples to the array of poems words
        poems_words_synset.append(temp)
    return poems_words_synset


# Get the synsets of poems words
poems_words_synset = get_synsets()


def debug(limit):
    for i, p_words in zip(range(limit), poems_words_synset):
        # print(p_words, '\n')
        print('\n', pos_tags[i], '\n')
        for words in p_words:
            print(words)
    print('\n')


# debug(10)


# def debug2(limit):
#     for i, p_words in zip(range(limit), alt_pos_tags):
#         # print(p_words, '\n')
#         print('\n', pos_tags[i], '\n')
#         for words in p_words:
#             print(words)
#     print('\n')


# debug2(10)


# def create_synset(word):
#     synsets = []
#     for i, word_pos in zip(range(10), pos_tags[1]):
#         word, pos = word_pos
#         syn = word + '.' + str(pos[0].lower()) + '.01'
#         synsets.append(syn)
#     print(synsets)
#     return synsets


def id_pos(word_tuple):
    # print(word_tuple)
    word, pos = word_tuple
    if pos.startswith('J'):
        return wordnet.ADJ
    elif pos.startswith('N'):
        return wordnet.NOUN
    elif pos.startswith('V'):
        return wordnet.VERB
    elif pos.startswith('R'):
        return wordnet.ADV
    else:
        return None


def make_synset_key(word_tuple):
    word, pos = word_tuple
    pos = id_pos(word_tuple)
    if pos is not None:
        return word + '.' + id_pos(word_tuple) + '.1'
    return None


def passing_thresh(threshold, w1, w2):

    if w1.wup_similarity(w2) >= threshold:
        return True
    return False


def unpack_synset(syn):
    return syn.split('.')[0]


def make_synset(word_tuple):
    try:
        word, pos = word_tuple
        pos_n = id_pos(word_tuple)
        return wordnet.synsets(word, pos=pos_n)
    except:
        return None


def generate_synsets():
    with open('../sent_dict.json', 'rb') as f:
        sent_dict = json.load(f)
    syn_sets = []
    # Go through each poem
    for i, poem in zip(range(2), poems_words):
        poem_syns = []
        # print('\n', 'i:', i, ':', poem)
        # print(len(poem), '\n')
        # Go through each word in the poem
        for j, word in enumerate(pos_tags[i]):
            if word is not '':
                key = id_pos(word)
                if key is not None:
                    syn_set = make_synset(word)
                    compare = True
                    try:
                        syn_comp = wordnet.synset(make_synset_key(word))
                    except:
                        syn_comp = None
                        compare = False

                    # print(word, ':', j, ':', make_synset_key(word), ':', make_synset(word), '\n')
                    set_of_syns = set()
                    # Go through the synonyms
                    for syn in syn_set:
                        if compare:
                            comparison = syn_comp.path_similarity(syn)
                        else:
                            comparison = 0

                        if comparison is None:
                            comparison = 0
                        # print(make_synset_key(word), ':', syn.name(), '=', comparison)
                        set_of_syns.add(unpack_synset(syn.name()))
                    poem_syns.append(set_of_syns)
                else:
                    poem_syns.append(set())
        syn_sets.append(poem_syns)

                        # print(unpack_synset(syn.name())[0], ':', make_synset_key(word), ':',
                        #  syn.wup_similarity(wordnet.synset(make_synset_key(word))))
                        # print(syn.name(), ':', make_synset_key(word), ':',
                        #       syn.wup_similarity(wordnet.synset(make_synset_key(word))))
                    # print('\n')
            #     else:
            #         print(word, ':', j, ':', key)
            # else:
            #     print(word)
    for i, poem in enumerate(poems_words):
        print(poem)
        for j, word in enumerate(poem):
            print(word, ':', syn_sets[i][j])
            # print(word, ':', syn, '\n')
            # print(syn)
        print('----------------------------------------------')


print(id_pos(('lain', 'NN')))
print(id_pos(('so', 'RB')))
print(id_pos(('missing', 'VBG')))



generate_synsets()


# Iterate through all poems
# Delimit the words in each poem
# and tag with a pos

# Use word, pos tag to make synset
# That makes sense to use. Grab the length
# of the set and set the iteration range
# to that length.


