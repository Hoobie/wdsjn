# coding=utf-8
import json
import operator
import re
from os.path import isfile

from plp import PLP

STIMULUS = 'mięso'

ALFA = 0.66

BETA = 0.00002


def pre_process(s):
    return re.sub('[^\w\s]', '', s.lower(), flags=re.UNICODE)


def strip_sie(form):
    if form.endswith(' się'):
        return form[:-len(' się')]
    return form


if __name__ == '__main__':
    p = PLP()
    with open('data/stop_words.json', 'r') as f:
        stop_list = json.load(f)

    words_freq = {}
    total_no = 0
    cooccurence_freq = {}
    associative_strength = {}

    if isfile('results/words_freq.json') and isfile('results/total_no.json') and isfile(
                            'results/' + STIMULUS + '_cooccurence_freq.json'):
        with open('results/words_freq.json', 'r') as f:
            words_freq = json.load(f)
        with open('results/total_no.json', 'r') as f:
            total_no = json.load(f)
        with open('results/' + STIMULUS + '_cooccurence_freq.json', 'r') as f:
            cooccurence_freq = json.load(f)
    else:
        with open('data/pap.txt', 'r') as f:
            pap = f.read().replace('\n', ' ').split('#')

        notes = {}

        for note in pap:
            if not re.search('\d{6}', note):
                continue

            note_id = re.findall('\d{6}', note)[0]
            note_content = re.sub(note_id, '', note).strip()

            words = pre_process(note_content).split(' ')
            for i, word in enumerate(words):
                if not p.rec(word):
                    continue

                basic_form = p.bform(p.rec(word)[0])
                if basic_form in stop_list:
                    continue

                # words frequencies and total words number
                word = strip_sie(basic_form)
                if word in words_freq:
                    words_freq[word] += 1
                else:
                    words_freq[word] = 1
                total_no += 1

                # co-occurence frequencies
                if word == STIMULUS:
                    min_idx = min(0, i - 12)
                    max_idx = min(len(words) - 1, i + 12)
                    window = words[min_idx:max_idx]
                    for neighbor in window:
                        if not p.rec(neighbor):
                            continue
                        basic_form = p.bform(p.rec(neighbor)[0])
                        if basic_form == STIMULUS or basic_form in stop_list:
                            continue
                        neighbor = strip_sie(basic_form)
                        if neighbor in cooccurence_freq:
                            cooccurence_freq[neighbor] += 1
                        else:
                            cooccurence_freq[neighbor] = 1

        with open('results/words_freq.json', 'w') as f:
            json.dump(words_freq, f)
        with open('results/total_no.json', 'w') as f:
            json.dump(total_no, f)
        with open('results/' + STIMULUS + '_cooccurence_freq.json', 'w') as f:
            json.dump(cooccurence_freq, f)

    print("total words number: " + str(total_no))

    # Rapp-Wettler algorithm
    for cooccurence, freq in cooccurence_freq.items():
        strength = 0
        neighbour_freq = words_freq[cooccurence]
        if neighbour_freq > BETA * total_no:
            strength = freq / pow(neighbour_freq, ALFA)
        else:
            strength = freq / (BETA * total_no)
        associative_strength[cooccurence] = strength
    sorted_associations = sorted(associative_strength.items(), key=operator.itemgetter(1), reverse=True)

    with open('results/' + STIMULUS + '_associations.csv', 'w', encoding='utf-8') as f:
        for association in sorted_associations:
            f.write(association[0] + "," + str(association[1]) + "\r\n")

    print(sorted_associations[0:10])
