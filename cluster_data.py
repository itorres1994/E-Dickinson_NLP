import json
import pickle

with open('AS_dict.json', 'rb') as f:
    as_dict = json.load(f)

with open('ed_themes_300.pickle', 'rb') as f:
    ed_themes = pickle.load(f)

with open('sent_dict.json', 'rb') as f:
    sent_dict = json.load(f)

sorted_as_dict = sorted(as_dict.items(), key=lambda e: int(e[0]))
sorted_as_dict = {item[0]: item[1] for item in sorted_as_dict}

sorted_ed_themes = sorted(ed_themes.items(), key=lambda e: int(e[0]))
sorted_ed_themes = {item[0]: item[1] for item in sorted_ed_themes}

missing = 0
available = 0
poem_theme_scores = []

for item in sorted_ed_themes:
    key = str(item)
    theme1, theme2 = sorted_ed_themes[item]
    try:
        score1 = sent_dict[theme1]
        available += 1
    except KeyError:
        score1 = None
        missing += 1
    try:
        score2 = sent_dict[theme2]
        available += 1
    except KeyError:
        score2 = None
        missing += 1

    if score1 is not None:
        if score2 is not None:
            poem_theme_scores.append((item, sorted_as_dict[key], [theme1, theme2],[score1, score2]))
        else:
            poem_theme_scores.append((item, sorted_as_dict[key], [theme1], [score1]))
    else:
        if score2 is not None:
            poem_theme_scores.append((item, sorted_as_dict[key], [theme2], [score2]))

    # print(item, ':', sorted_ed_themes[item])

poem_theme_scores = sorted(poem_theme_scores, key=lambda e: (e[1][0], e[3][0]))

for poem in poem_theme_scores:
    print(poem)

print(missing, '/', available)
