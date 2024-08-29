# Requires the following packages: pyphen, pandas, numpy
# Takes '-' hyphen as input

print('Starting Syllabificator...')

import pandas as pd
import re
import unicodedata
import logging
import warnings

# Suppress superfluous 'deprecated' warning upon loading CRF-keras
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

from algorithms import algo_brandt, algo_liang, algo_crf, algo_weijters, algo_neural
from algorithms import algo_neural_eng  # For english NN
from scripts import analyze

print('Libraries imported successfully.')

brandt_syl = algo_brandt.brandt_syllabificate
liang_syl = algo_liang.liang_syllabificate
crf_syl = algo_crf.crf_syllabificate
weijters_syl = algo_weijters.weijters_syllabificate
nn_syl = algo_neural.nn_syllabificate
nn_syl_eng = algo_neural_eng.nn_syllabificate

run_analysis = analyze.analyze_set
    
# Function for dehyphenating
def dehyphenate(word):
    return word.replace('-', '')

# Imput as pandas series containing correct hyphenations. Set
# print option to false to toggle help file
def run_all(reference_set, print_info=True):

    dehyphenated = reference_set.apply(dehyphenate)

    brandt_set = dehyphenated.apply(brandt_syl)
    liang_set = dehyphenated.apply(liang_syl)
    crf_set = dehyphenated.apply(crf_syl)
    weijters_set = dehyphenated.apply(weijters_syl, checks=200)
    nn_set = dehyphenated.apply(nn_syl)
    # x_set = dehyphenated.apply(algorithm_of_choice) to easily add another algorithm
    # y_set etc.

    print('Running algorithm performance analysis.')
    print('Note that the default naming order for Dataset 1 through 5 is Brandt, Liang, CRF, Weijters, NN')
    output = run_analysis(reference_set,
                          brandt_set,
                          liang_set,
                          crf_set,
                          weijters_set,
                          nn_set,
                        # x_set, y_set,
                          print_help=print_info)

    return output

# For running hyphenated lists against each other. Input is x series of
# which first is the solution (reference set)
def run_sets(*input_datasets, print_info=True):

    output = run_analysis(*input_datasets,
                          print_help=print_info)

# For hyphenating individual word. 'alg' selects which algorithm to use.
# The neural net is trained for a max word length of 34/22 characters.
def syllabificate_word(word, alg='c', pattern=2, w_size=20, language='nl'):

    if alg=='l':
        hyphenated = liang_syl(word)
    if alg=='b':
        hyphenated = brandt_syl(word)
    if alg=='c':
        hyphenated = crf_syl(word, language)
    if alg=='w':
        hyphenated = weijters_syl(word, checks=w_size)
    if alg=='n':
        if language=='nl' and len(word)<35:
            hyphenated = nn_syl(word)
        elif language=='nl' and len(word)>=35:
            hyphenated = crf_syl(word)
            print('Word with length>34 detected, replacing with CRF')
        if language=='eng' and len(word)<23:
            hyphenated = nn_syl_eng(word)
        elif language=='eng' and len(word)>=23:
            hyphenated = crf_syl(word, language)
            print('Word with length>22 detected, replacing with CRF')

    return hyphenated

# Quick function to remove accents to remove special characters (e.g. 'é')
def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

# Syllabificate a document. Numbers are ignored, special characters removed
def syllabificate_text(text, alg='c', pattern=2, w_size=2000, language='nl'):

    split_text = re.split(r'(\W|_)', remove_accents(text))
    output = []

    # Syllabificate each words, capitals are removed and reinserted
    for section in split_text:
        if section.isalpha() == False:
            output.append(section)
            continue

        word = section
        word_original = word
        capitals = re.finditer('[A-Z]', word)
        word = word.lower()

        hyphenated = syllabificate_word(word, alg, pattern, w_size, language)

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

print('To syllabify text, use syllabificate_text(\'Een bepaalde tekststring.\')')

