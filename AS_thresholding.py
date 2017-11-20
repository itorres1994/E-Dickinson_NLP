import json

with open('sent_dict.json', 'rb') as f:
    sent_dict = json.load(f)

with open('AS_dict.json', 'rb') as f:
    as_dict = json.load(f)

sorted_as_dict = sorted(as_dict.items(), key=lambda e: int(e[0]))
sorted_as_dict = {item[0]: item[1] for item in sorted_as_dict}

# human_pred_ian = open('human_affect_pred_ian.txt').read()
# human_pred_trev = open('human_affect_pred_trev.txt').read()
#
# human_pred_ian = human_pred_ian.split('\n')
# human_pred_trev = human_pred_trev.split('\n')

# human_pred_ian.remove('')

# pred_ian = []
# pred_trev = []
# for j, pred in enumerate(human_pred_ian):
#     pred_split = pred.split(' ')
#     i = pred_split[0][:pred_split[0].index(':')]
#     pred_ian.append((int(i), pred_split[1]))
#
#     pred_split = human_pred_trev[j].split(' ')
#     i = pred_split[0][:pred_split[0].index(':')]
#     pred_trev.append((int(i), pred_split[1]))
#
# correct_trev = 0
#
# for i, key in zip(range(len(pred_ian)), sorted_as_dict):
#     if pred_trev[i][1] == 'pos' and sorted_as_dict[key][0] > 0:
#         print('True')
#         correct_trev += 1
#     else:
#         if pred_trev[i][1] == 'neg' and sorted_as_dict[key][0] < 0:
#             print('True')
#             correct_trev += 1
#         else:
#             print('False')
#     print(key, ':', pred_ian[i][1], ',', pred_trev[i][1], ' - ', sorted_as_dict[key],
#           ' = ', pred_ian[i][1] == pred_trev[i][1], '\n')
#
# print('# correct/# total', ':', correct_trev, '/', len(pred_trev))


# bins: [[-0.4, -0.3), [-0.3, -0.2), [-0.2, -0.1), [-0.1, 0.0), [0.0, 0.1), [0.1, 0.2), [0.2, 0.3]]
bins = [0, 0, 0, 0, 0, 0, 0]
bins2 = [0, 0]

for item in sorted_as_dict:
    number = round(sorted_as_dict[item][0], 3)
    if -0.4 <= number < -0.3:
        bins[0] += 1
    elif -0.3 <= number < -0.2:
        bins[1] += 1
    elif -0.2 <= number < -0.1:
        bins[2] += 1
    elif -0.1 <= number < 0.0:
        bins[3] += 1
    elif 0.0 <= number < 0.1:
        bins[4] += 1
    elif 0.1 <= number < 0.2:
        bins[5] += 1
    else:
        bins[6] += 1
    # print(round(sorted_as_dict[item][0], 3))

for item in sorted_as_dict:
    number = round(sorted_as_dict[item][0], 3)
    if number < 0:
        bins2[0] += 1
    else:
        bins2[1] += 1

print(bins)
print(bins2)

# bins: [[-0.4, -0.35), [-0.35, -0.30), [-0.30, -0.25), [-0.20, -0.15), [-0.15, -0.10), [-0.10, -0.05), [0.05, 0.0),
# [0.0, 0.05), [0.05, 0.10), [0.10, 0.15), [0.15, 0.20), [0.20, 0.25), [0.25, 0.3]]
bins3 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for item in sorted_as_dict:
    number = round(sorted_as_dict[item][0], 3)
    if -0.4 <= number < -0.35:
        bins3[0] += 1
    elif -0.35 <= number < -0.3:
        bins3[1] += 1
    elif -0.3 <= number < -0.25:
        bins3[2] += 1
    elif -0.25 <= number < -0.2:
        bins3[3] += 1
    elif -0.2 <= number < -0.15:
        bins3[4] += 1
    elif -0.15 <= number < -0.1:
        bins3[5] += 1
    elif -0.1 <= number < -0.05:
        bins3[6] += 1
    elif -0.05 <= number < 0.0:
        bins3[7] += 1
    elif 0.0 <= number < 0.05:
        bins3[8] += 1
    elif 0.05 <= number < 0.1:
        bins3[9] += 1
    elif 0.1 <= number < 0.15:
        bins3[10] += 1
    elif 0.15 <= number < 0.20:
        bins3[11] += 1
    elif 0.20 <= number < 0.25:
        bins3[12] += 1
    else:
        bins3[13] += 1

print(bins3)
