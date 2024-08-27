# See Trogkanis 2010 for detailed description of various metrics used

import pandas as pd
import numpy as np

# Analyze correct word set against input set(s)
# Takes '-' as valid hyphenation character on input

def dehyphenate(word):

    return word.replace('-', '')

def analyze_set(correct_set, *input_datasets, print_help = False):

    input_sets = list(input_datasets)

    dataset_names = []

    # Set names for output in the dataframe:

    for data in range(len(input_sets)):
        print('Please input name of dataset ' + str(data+1) +
              ' (for display purposes):')
        data_name = input()
        dataset_names = dataset_names + [data_name]

    dataset_names = dataset_names + ['NO_HYPHEN', 'CORRECT']
        
    column_names = ['TP', 'FP', 'TN', 'FN', 'owe', 'swe', '%ower',
                    '%swer', '%oler', '%sler']
    
    output_frame = pd.DataFrame(np.zeros((len(dataset_names),10)),
                                columns = column_names,
                                index = dataset_names)

    # For the dehyphenated ['NO_HYPHEN'] set

    dehyphenated_set = correct_set.copy()
    dehyphenated_set = dehyphenated_set.apply(dehyphenate)

    input_sets = input_sets + [dehyphenated_set] + [correct_set] 

    output_frame['TP'] = output_frame['TP'].astype(np.int64)
    output_frame['FP'] = output_frame['FP'].astype(np.int64)
    output_frame['TN'] = output_frame['TN'].astype(np.int64)
    output_frame['FN'] = output_frame['FN'].astype(np.int64)
    output_frame['owe'] = output_frame['owe'].astype(np.int64)
    output_frame['swe'] = output_frame['swe'].astype(np.int64)

    correct_set_length = len(correct_set)

    for dataset in input_sets:
        if len(dataset) != correct_set_length:
            print('Error detected: input datasets are of incompatible length, '
                  + 'please verify datasets have same length.')

    # Block for processing errors

    parse = round(len(correct_set)/10)
    counter_list = [f'parse*{i}' for i in range(1, 10)]
        
    print('Processing...')

    for word in range(len(correct_set)):

        for dataset in range(len(input_sets)):

            correct_word = correct_set.iloc[word]
            hyph_word = input_sets[dataset].iloc[word]
            
            tp, fp, fn, tn, owe, swe = evaluate_word(correct_word, hyph_word)
            
            output_frame.loc[dataset_names[dataset], 'TP'] += tp
            output_frame.loc[dataset_names[dataset], 'FP'] += fp
            output_frame.loc[dataset_names[dataset], 'TN'] += tn
            output_frame.loc[dataset_names[dataset], 'FN'] += fn
            output_frame.loc[dataset_names[dataset], 'owe'] += owe
            output_frame.loc[dataset_names[dataset], 'swe'] += swe

        if str(word)[-2:] == '00':

            print(word)
            
    # For analyzing owe/se/ower/swer
    
    for dataset in range(len(input_sets)):

        owe_value = output_frame.loc[dataset_names[dataset], 'owe']
        owe_calculated = owe_value / correct_set_length
        output_frame.loc[dataset_names[dataset], '%ower'] = round(owe_calculated * 100, 3)

        swe_value = output_frame.loc[dataset_names[dataset], 'swe']
        swe_calculated = swe_value / correct_set_length
        output_frame.loc[dataset_names[dataset], '%swer'] = round(swe_calculated * 100, 3)

        tp = output_frame.loc[dataset_names[dataset], 'TP']
        fp = output_frame.loc[dataset_names[dataset], 'FP']
        tn = output_frame.loc[dataset_names[dataset], 'TN']
        fn = output_frame.loc[dataset_names[dataset], 'FN']

        oler = (fp + fn) / (tp + tn + fp + fn)
        sler = fp / (tp + tn + fp + fn)

        output_frame.loc[dataset_names[dataset], '%oler'] = round(oler * 100, 3)
        output_frame.loc[dataset_names[dataset], '%sler'] = round(sler * 100, 3)

    reindex_order = [dataset_names[-1]] + [dataset_names[-2]] + dataset_names[:-2]

    output_frame = output_frame.reindex(reindex_order)

    print(output_frame)

    if print_help == True:
        print('\nTable description:\n' + 
        'CORRECT constrasts the original dataset with itself (FP/FN should '
        'be 0).\nNO_HYPHEN lists the original dataset with hyphens removed as a reference ' +
        'set.\n\nAbbrevations:\nTP = True Positives (hyphens predicted correctly)' +
        '\nTN = True Negatives (hyphens predicted incorrectly)\nTN = True Negatives ' +
        '(hyphens correctly not predicted)\nFN = False Negatives (hyphens failed to be '
        'predicted)\nowe = Overall Word-level Errors (words with at least one FP or FN)' +
        '\nswe = Serious Word-level Errors (words with at least one FP)\n%ower = ' +
        'Overall Word-level Error Rate (owe / total words)\n%swer = Serious Word-' +
        'level Error Rate (swe / total words)\n%oler = Overall Letter-level Error Rate ' +
        '([FP+FN] / [TP+TN+FP+FN])\n%sler = Serious Letter-level Error Rate ' +
        '(FP / [TP+TN+FP+FN])')
        print()

    return output_frame

# Return list with letter positions that are followed by hyphen

def hyph_positions(hyphenated_word):

    output = []

    for char in range(len(hyphenated_word)-1):
        if hyphenated_word[char+1] == '-':
            output = output + [char - len(output)]  # Sub 1 to offset hyphens

    return output
        
# Return various parametrics

def evaluate_word(correct_word, input_word):

    input_w = hyph_positions(input_word)
    correct_w = hyph_positions(correct_word)

    tp = len(set(input_w) & set(correct_w))  # True positive
    fp = len(set(input_w) - set(correct_w))  # False positive
    fn = len(set(correct_w) - set(input_w))  # False negative
    tn = len(set(range(len(correct_word)-len(correct_w)-1)) - set(correct_w) &
          set(range(len(input_word)-len(input_w)-1)) - set(input_w))
                        #  True negative
    owe = (fp > 0 or fn > 0)
    swe = fp > 0
    
    return [tp, fp, fn, tn, owe, swe]
