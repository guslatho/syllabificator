# Requires the following packages: pyphen, pandas, numpy
# Takes '-' hyphen as input

import pandas as pd
import re

import algo_brandt
import algo_liang
import algo_crf
import algo_weijters
import analyze

brandt_hyphen = algo_brandt.brandt_hyphenate
liang_hyphen = algo_liang.liang_hyphenate
crf_hyphen = algo_crf.crf_hyphenate
weijters_hyphen = algo_weijters.weijters_hyphenate
run_analysis = analyze.analyze_set

    
# Function for dehyphenating
def dehyphenate(word):

    return word.replace('-', '')

# Imput reference set as word series containing correct hyphenations. Set
# print option to false to toggle help file
def run_all(reference_set, print_info=True):

    dehyphenated = reference_set.apply(dehyphenate)

    brandt_set = dehyphenated.apply(brandt_hyphen)
    liang_set = dehyphenated.apply(liang_hyphen)
    crf_set = dehyphenated.apply(crf_hyphen)
    weijters_set = dehyphenated.apply(weijters_hyphen, checks=200)
    # x_set = dehyphenated.apply(algorithm_of_choice) to easily add another algorithm
    # y_set etc.

    output = run_analysis(reference_set,
                          brandt_set,
                          liang_set,
                          crf_set,
                          weijters_set,
                        # x_set, y_set,
                          print_help=print_info)

    return output

# For running hyphenated lists against each other. Input is x series of
# which first is the solution (reference set)
def run_sets(*input_datasets, print_info=True):

    output = run_analysis(*input_datasets,
                          print_help=print_info)

# For hyphenating individual word. 'alg' selects which algorithm to use.
def hyphenate_word(word, alg='l', pattern=2, w_size=2000):

    if alg=='l':
        hyphenated = liang_hyphen(word, library=pattern)
    if alg=='b':
        hyphenated = brandt_hyphen(word)
    if alg=='c':
        hyphenated = crf_hyphen(word)
    if alg=='w':
        hyphenated = weijters_hyphen(word, checks=w_size)

    return hyphenated

# Hyphenate a document. Numbers are ignored.
def hyphenate_text(text, alg='c', pattern=2, w_size=2000):

    split_text = re.split(r'(\W|_)', text)

    output = []

    # Hyphenate each words, capitals are removed and reinserted
    for section in split_text:

        if section.isalpha() == False:
            output.append(section)
            continue

        word = section
        word_original = word
        capitals = re.finditer('[A-Z]', word)
        word = word.lower()

        hyphenated = hyphenate_word(word, alg, pattern, w_size)

        hyphens_positions = ([hyphenated[i+1] == '-' for i in
                              range(len(hyphenated)-1)
                              if hyphenated[i]!= '-'] + [False])
        word_output = []

        # Rejoin the capatalized version
        for letter in range(len(word)):
            if hyphens_positions[letter] == True:
                word_output.append(word_original[letter]+'-')
            else:
                word_output.append(word_original[letter])

        output.append(''.join(word_output))


    return ''.join(output)

#Short hand
ht = hyphenate_text
hw = hyphenate_word

print('Syllabificator initialized successfully.')
print('To syllabify text, use hyphenate_text(\'Een bepaalde tekststring.\')')



