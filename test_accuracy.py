import pickle
import json

with open('./affect_tags.pickle', 'rb') as f:
    affect_tags = pickle.load(f)

with open('./AS_dict.json', 'rb') as f:
    as_dict = json.load(f)

eval = []

print(list(affect_tags.items()))

print(len(as_dict))
for i, tag in enumerate(as_dict):
    if i < len(as_dict)-1:
        if as_dict[tag][0] >= 0:
            affect = 1
        else:
            affect = 0
        bool_val = affect == affect_tags[i+1]
        eval.append(bool_val)

for i, e in zip(range(10), eval):
    print(i, ':', e)
