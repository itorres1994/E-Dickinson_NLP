import re
import nltk

f = open("edCompleteFormatted.txt", 'r').read()

poem_dict = {i: poem.replace('\n', '').split(" ") for i, poem in enumerate(re.split(r'[0-9]+', f))}

for poem in poem_dict:
    for word in poem_dict[poem]:
        if "." in word or "," in word or "?" in word or "!" in word or ";" in word or "-" in word or "\"" in word \
                or "\'" in word:
            # print(word)
            correction = re.split(r'\.|,|\?|-|\"|!|;|\'', word)
            # print(correction)
            if '' in correction:
                count = correction.count('')
                for c in range(count):
                    correction.remove('')
            # print(correction)
            poem_dict[poem].remove(word)
            poem_dict[poem].extend(correction)
        else:
            if re.compile(r'[a-z]+[A-Z]+').match(word):
                # print(word)
                # print(re.search(r'[A-Z]', word))
                indexL, _ = re.search(r'[A-Z]', word).span()
                # print(index)
                correction = [word[:indexL], word[indexL:]]
                # print(correction)
                poem_dict[poem].remove(word)
                poem_dict[poem].extend(correction)
            if re.compile(r'[A-Z][a-z]+[A-Z]').match(word):
                # print(word)
                # print(re.search(r'[a-z][A-Z]', word))
                indexL, indexR = re.search(r'[a-z][A-Z]', word).span()
                # print(index)
                correction = [word[:indexR - 1], word[indexL + 1:]]
                # print(correction)
                poem_dict[poem].remove(word)
                poem_dict[poem].extend(correction)

print('\n\n')

# for poem in poem_dict:
#     print(poem_dict[poem])
#
# proximity_dict = dict()
#
# for poem in poem_dict:
#     poem_words = poem_dict[poem]
#     for word in poem_words:
#         # if not word == '':
#         if word not in proximity_dict:
#             proximity_dict[word] = dict()
#         for w in poem_words:
#             if not w == word:
#                 if w in proximity_dict[word]:
#                     if w in proximity_dict:
#                         if word in proximity_dict[w]:
#                             proximity_dict[w][word] += 1
#                         else:
#                             proximity_dict[w][word] = 1
#                     else:
#                         proximity_dict[w] = dict()
#                     proximity_dict[word][w] += 1
#                 else:
#                     if w in proximity_dict:
#                         if word in proximity_dict[w]:
#                             proximity_dict[w][word] += 1
#                         else:
#                             proximity_dict[w][word] = 1
#                     else:
#                         proximity_dict[w] = dict()
#                     proximity_dict[word][w] = 1
#
# # for line in f.split("\n"):
# #     words = line.split(" ")
# #     if re.compile(r'[a-zA-Z]+').match(line):
# #         print(line)
# #         for i, word in zip(range(len(words) - 1), words):
# #             if re.compile(r'[a-zA-Z]+').match(word):
# #                 if i == 0:
# #                     print(word, "_", words[i+1])
# #                 else:
# #                     print(words[i-1], "_", word, "_", words[i+1])
#
# sorted_word = sorted(proximity_dict.items(), key=lambda e: sum(e[1].values()), reverse=True)
# sorted_word = {word[0]: word[1] for word in sorted_word if not word[0] == ''}
#
# # for word in sorted_word:
# #     print(word, ":", len(sorted_word[word].keys()))
# #     # print(word, ":\n", sorted_word[word].keys(), '\n')
#
# # for word in proximity_dict:
# #     print(word, ':', proximity_dict[word], '\n')
