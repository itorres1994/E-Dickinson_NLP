from shutil import copyfile
import os
import pickle

with open('affect_tags.pickle', 'rb') as f:
    affect_tags = pickle.load(f)

path_dir = './edCompleteSimple'
out_dir = './training_ed'
pos = 'pos'
neg = 'neg'
list_dir = os.listdir(path_dir)
list_dir = sorted(list_dir, key=lambda e: int(e.split('.')[0]))

print(list_dir[:10])  # Debug statement

file_listing = [(f, os.path.join(path_dir, f)) for f in list_dir]

print(file_listing[:10])  # Debug statement
# print(affect_tags['1'])
tags = [a for a in affect_tags.items()]
# tags = sorted(tags, key=lambda e: int(e[0]))
print(tags[0])
tags = {str(t[0]): int(t[1]) for t in tags}

print(list(tags)[:10])  # Debug statement

# print(affect_tags['102'])  # Debug statement: KeyError

for i, t in enumerate(file_listing):
    file_name, file_path = t
    tag = i + 1
    try:
        if affect_tags[tag] == 0:
            copyfile(file_path, os.path.join(out_dir, neg, file_name))
        else:
            copyfile(file_path, os.path.join(out_dir, pos, file_name))
        print(t)
    except KeyError:
        print('key ->', tag, ', does not exist')

