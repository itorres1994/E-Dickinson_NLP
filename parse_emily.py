import re
import nltk

f = open("edCompleteFormatted.txt", 'r').read()

tokens = nltk.word_tokenize(f)
tagged_tokens = nltk.pos_tag(tokens)

freq_dict = dict()

for token, pos in tagged_tokens:
    token_reg = token.lower().replace('-', '')
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
        key = token_reg, pos
        if key in freq_dict:
            freq_dict[key] = freq_dict[key] + 1
        else:
            freq_dict[key] = 1

sorted_freq = sorted(freq_dict.items(), key=lambda e: e[1], reverse=True)

print('\n\n')

for freq in sorted_freq:
    print(freq)

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

