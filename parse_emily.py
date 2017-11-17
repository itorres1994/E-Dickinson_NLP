import re
import nltk
import json

f = open("edCompleteFormatted.txt", 'r').read()

tokens = nltk.word_tokenize(f)
tagged_tokens = nltk.pos_tag(tokens)
count_poem = 0

freq_dict = dict()
word_dict = dict()

for token, pos in tagged_tokens:
    token_reg = token.lower().replace('-', '').replace('.', '')
    if pos == 'CD':
        count_poem += 1
    else:
        if re.compile(r'[a-z]+').match(token_reg) and not token_reg == 'is' and not pos == '``'\
                and not token_reg == 'am' and not token_reg == 'are' and not token_reg == 'was'\
                and not token_reg == 'were' and not token_reg == 'be' and not token_reg == 'being'\
                and not token_reg == 'been' and not token_reg == 'have' and not token_reg == 'has'\
                and not token_reg == 'had' and not token_reg == 'do' and not token_reg == 'does' \
                and not token_reg == 'did' and not token_reg == 'shall' and not token_reg == 'will' \
                and not token_reg == 'should' and not token_reg == 'would' and not token_reg == 'may' \
                and not token_reg == 'might' and not token_reg == 'must' and not token_reg == 'can' \
                and not token_reg == 'could' and not token_reg == "'":
            if token_reg in word_dict:
                if pos in word_dict[token_reg]['FREQ']:
                    word_dict[token_reg]['FREQ'][pos] += 1
                else:
                    word_dict[token_reg]['POS'].append(pos)
                    word_dict[token_reg]['FREQ'][pos] = 1
            else:
                word_dict[token_reg] = {'POS': [pos],
                                        'FREQ': {
                                            pos: 1
                                         }
                                        }

    if not pos == 'CD' and not pos == 'IN' and not pos == 'EX' \
            and not pos == 'LS' and not pos == "TO" and not pos == 'SYM' \
            and not pos == '.' and not pos == 'DT' and not pos == ','\
            and not pos == '$' and not pos == "''" and not pos == '(' and not pos == ')'\
            and not pos == ',' and not pos == '--' and not pos == ':' and not pos == 'PRP'\
            and not pos == 'CC' and not pos == 'PRP$' and not token_reg == 'is' and not pos == '``'\
            and not token_reg == 'am' and not token_reg == 'are' and not token_reg == 'was'\
            and not token_reg == 'were' and not token_reg == 'be' and not token_reg == 'being'\
            and not token_reg == 'been' and not token_reg == 'have' and not token_reg == 'has'\
            and not token_reg == 'had' and not token_reg == 'do' and not token_reg == 'does' \
            and not token_reg == 'did' and not token_reg == 'shall' and not token_reg == 'will' \
            and not token_reg == 'should' and not token_reg == 'would' and not token_reg == 'may' \
            and not token_reg == 'might' and not token_reg == 'must' and not token_reg == 'can' \
            and not token_reg == 'could' and not token_reg == "'":
        key = token_reg
        if key in freq_dict:
            if pos in freq_dict[key]['FREQ']:
                freq_dict[key]['FREQ'][pos] += 1
            else:
                freq_dict[key]['POS'].append(pos)
                freq_dict[key]['FREQ'][pos] = 1
        else:
            freq_dict[key] = {'POS': [pos],
                              'FREQ': {
                                  pos: 1
                               }
                              }

sorted_freq = sorted(freq_dict.items(), key=lambda e: sum(e[1]['FREQ'].values()), reverse=True)
sorted_word = sorted(word_dict.items(), key=lambda e: sum(e[1]['FREQ'].values()), reverse=True)
sorted_word = {word[0]: word[1] for word in sorted_word}

print('\n\n*************************Possible Seeds*************************\n\n')

for freq in sorted_freq:
    if len(freq[1]['POS']) >= 5:
        print(freq)

print('\n\n*************************Words*************************\n\n')

for freq in sorted_word:
    print(freq, ":", sorted_word[freq])

print(count_poem)

with open('emily_freq.json', 'w') as f:

    json.dump(sorted_word, f)

print('Done')

# for freq in sorted_freq:
#     print(freq)

# lines = []
#
#
# # Parse all of the lines in the file then parse the lines by word
# # Get rid of any punctuation
# for line in f:
#     if not re.compile(r'[0-9]+').match(line) and not line == '\n':
#         lines.append(line.replace('\n', '').replace(',', '').
#                      replace('.', '').replace('!', '').replace('?', '').
#                      replace('!', '').replace('-', '').split(" "))
#
# f.close()
#
# freq_dict = dict()
#
# for line in lines:
#     for word in line:
#         if word in freq_dict:
#             freq_dict[word] = freq_dict[word] + 1
#         else:
#             freq_dict[word] = 1
#
# print(lines[:20])
#
# print(list(freq_dict.items())[:20])

