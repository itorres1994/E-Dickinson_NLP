from shutil import copyfile
import os
import pickle

with open('affect_tags.pickle', 'rb') as f:
    affect_tags = pickle.load(f)

path_dir = './edCompleteSimple'
out_dir = './E-Dickinson_dataset/train'
out2_dir = './E-Dickinson_dataset/test'
pos = 'pos'
neg = 'neg'
list_dir = os.listdir(path_dir)
list_dir = sorted(list_dir, key=lambda e: int(e.split('.')[0]))

# print(list_dir[:10])  # Debug statement

file_listing = [(f, os.path.join(path_dir, f)) for f in list_dir]

# print(file_listing[:10])  # Debug statement
# print(affect_tags['1'])
tags = [a for a in affect_tags.items()]
# tags = sorted(tags, key=lambda e: int(e[0]))
# print(tags[0])
tags = {str(t[0]): int(t[1]) for t in tags}

# print(list(tags)[:10])  # Debug statement

# print(affect_tags['102'])  # Debug statement: KeyError

pos_poems = []
neg_poems = []
for t in affect_tags:
    if affect_tags[t] == 0:
        neg_poems.append(t)
    else:
        pos_poems.append(t)

print(len(pos_poems))
print(len(neg_poems))

train_pos = pos_poems[:int(len(pos_poems) * 0.7) + 1]
test_pos = pos_poems[int(len(pos_poems) * 0.7) + 1:]

train_neg = neg_poems[:int(len(neg_poems) * 0.7) + 1]
test_neg = neg_poems[int(len(neg_poems) * 0.7) + 1:]

print(train_pos)
print('\n\n\n')
print(train_neg)
# print(len(train_pos), '+', len(test_pos))
# print(len(train_neg), '+', len(test_neg))

count_train_pos = count_train_neg = count_test_pos = count_test_neg = 0
for i, t in enumerate(file_listing):
    file_name, file_path = t
    tag = i + 1
    try:
        if tag in train_neg:
            count_train_neg += 1
            copyfile(file_path, os.path.join(out_dir, neg, file_name))
        elif tag in test_neg:
            count_test_neg += 1
            copyfile(file_path, os.path.join(out2_dir, neg, file_name))
        elif tag in train_pos:
            count_train_pos += 1
            copyfile(file_path, os.path.join(out_dir, pos, file_name))
        else:
            count_test_pos += 1
            copyfile(file_path, os.path.join(out2_dir, pos, file_name))
    # print(t)
    except KeyError:
        print('key ->', tag, ', does not exist')

print('train pos ->', count_train_pos)
print('test pos ->', count_test_pos)

print('train neg ->', count_train_neg)
print('test neg ->', count_test_neg)
