import pandas as pd
import numpy as np
import time

dictionary_name = 'dictionary_celex.csv'

DICTIONARY = pd.read_csv(dictionary_name, header = None)
WINDOW = 7
WEIGHTS = [1, 4, 16, 64, 16, 4, 1]
MOD_VALUE = 3
HYPHEN = '-'

# Execution of weijters (1991) algorithm. Best read from bottom to top
# (main function at very bottom called hyphenate_weijers)


# Dehyphenate a word, useful for comparison
def dehyphenate(word):

    return word.replace(HYPHEN, '')


# Get the positions of hyphens in a word (e.g., 'lo-pen-de' = [1, 4])
def hyph_positions(hyphenated_word):

    hyphenations_found = 0

    list_out = []

    for char in range(len(hyphenated_word)-1):
        if hyphenated_word[char+1] == HYPHEN:
            list_out.append(char-hyphenations_found)
            hyphenations_found += 1

    return list_out


# Contrasts two different strings and returns matrix (e.g. 'epel' and 'spel' -> [F,T,T,T])
def contrast_strings(word1, word2):

    match_list = []

    for char in range(len(word2)):

        if word1[char] == word2[char]:
            match_list.append(True)
        else:
            match_list.append(False)

    return match_list


# Small function to calculate distance for a boolean from middle, for weight selection
def convert_to_pos(distance):

    middle = round(len(WEIGHTS)/2 -0.1)
    return middle + distance


# Given a boolean list of comparison (result of window comparison), return score
def calculate_sum(boolean_list, center):

    summed_value = 0

    for boolean in range(len(boolean_list)):

        dist_from_center = convert_to_pos(boolean - center)
        
        weight_value = WEIGHTS[dist_from_center]
        summed_value += (weight_value * boolean_list[boolean])

    return summed_value

# Compares two words, word we want to hyph has a window, use this
# For instance:
# Word we want to hyphenate = 'vragende'
# Center character = 2, meaning we'll focus on 'a' in 'vragende'
# Window = [0, 1, <2>, 3, 4, 5], <2> = focus
# Reference word = 'werktaken'
# Cycle through 'werkta', 'erktak', 'rktake' etc and return match values for each

# toepakkens
# antakken
# 

def compare_words(word, reference_word, window, center):

    return_list = []

    # Store the window for word we want to hyphenate,
    # e.g. [0, 1, 2, 3, 4, 5] -> 'vragen'
    window_to_check_word = word[window[0]:window[-1]+1]

    # Center position in the window [4, 5, 6, 7, 8], case 7 = 3rd position
    center_position = window.index(center)

    # Word
    center_deviance_word = -5 + round(10/(len(word)-1) * center, 2)    

    # For each character in a window, compare it vs reference word
    for char in range(len(reference_word) - len(window)+1):

        # Window for reference word depending on the iteration (char) count
        reference_window = [i - window[0] + char for i in window]
        reference_center = reference_window[center_position]

        # Store the string for reference window, e.g. [1, 2, 3, 4, 5, 6] -> 'erktak'
        window_to_check_ref = reference_word[reference_window[0]:reference_window[-1]+1]

        # Contrast original window vs ref, e.g. 'vragen' vs 'ertak'
        contrast = contrast_strings(window_to_check_word,
                                    window_to_check_ref)

        # How well do these two match? Higher score = better match
        match_value = calculate_sum(contrast, center_position)

        # Modifier: to punish references 
        center_deviance_word_ref = -5 + round(10/(len(reference_word)-1) * reference_center, 2)
        center_synergy = center_deviance_word - center_deviance_word_ref
        match_value -= round((np.abs(center_synergy)*MOD_VALUE))
        if match_value<0:
            match_value = 0

        return_list.append(match_value)

    return return_list


# Getting a window enclosure for a specific character in a word.    
def get_window(word, character):

    window_left = character - 3 #
    window_right = character + 4 #

    if window_left < 0:
        window_left = 0
    if window_right > len(word):
        window_right = len(word)

    return list(range(window_left, window_right))


# Function for comparing two words against each other, spits out 'best results'
def do(word, hyphenated_word):

    # Get the hyphenated (reference) word and check where the hyphens are
    reference_word = dehyphenate(hyphenated_word)
    hyphenation_positions = hyph_positions(hyphenated_word)

    # For storing all the results
    list_score = [0 for i in word]
    hyphenation = [False for i in word]

    # For each character in the word we want to hyphenate, get a check vs the ref word
    # For instance, if word we want to hyphenate is 'plakken':
    # Start with '(p)lakken', then 'p(l)akken', etc.
    for char in range(len(word)-1):

        center = char

        # Build window around char.
        # E.g., 'p(l)akken' has center of 2, results in [0,1,2,3,4]
        window = get_window(word, center)

        # Compare the window of word we want to hyphenate vs ref word
        match_list = compare_words(word, reference_word, window, center)

        for value in range(len(match_list)):

            if match_list[value] > list_score[char]:
                list_score[char] = match_list[value]

                iteration = value
                center_position = window.index(center)
                reference_pos = iteration + center_position

                if reference_pos in hyphenation_positions:
                    hyphenation[char] = True
                else:
                    hyphenation[char] = False

    return list_score, hyphenation
    

        
# Main function. Set checks to amount of words you want to contrast against
def weijters_hyphenate(word, checks=0, print_toggle=False):

    # If left at default, run through whole dictionary. 
    if checks == 0:
        it = range(len(DICTIONARY.iloc[:,0]))
        
    # For random attacks. If checks set at e.g. 15, pick 15 random words
    if checks > 0:
        it = np.random.choice(len(DICTIONARY.iloc[:,0]),size=checks,replace=False).tolist() 

    grand_score_list = [0 for i in word]
    grand_hyphen_list = [False for i in word]
    grand_ref_list = ['x' for i in word]
       
    # Run comparison for word against x amount of words in dictionary list
    for check in it:

        # Retrieve word from dictionary, input it into the do function
        hyphen_word = DICTIONARY.iloc[check,0]

        values, booleans = do(word, hyphen_word)

        # If any character scores really well in reference word, store it
        for value in range(len(values)):
            if values[value] > grand_score_list[value]:

                print_m('New improved value found! Score ' + str(values[value])
                      + ' for character ' + str(value) + ' registered.', print_toggle)
                grand_score_list[value] = values[value]
                grand_hyphen_list[value] = booleans[value]
                grand_ref_list[value] = hyphen_word

    print_m('Word processing completed. Displaying best word match for '
          + 'each letter. Format is as follows: letter: best matching '
          + 'word, (insert hyphen based on reference or not), matching score.', print_toggle)

    for letter in range(len(grand_ref_list)):

        print_m(word[letter] + ': ' + str(grand_ref_list[letter])
              + ' (' + str(grand_hyphen_list[letter]) + '), '
              + str(grand_score_list[letter]), print_toggle)

    return_word = []

    # For pasting the word together for the output
    for letter in range(len(word)):

        return_word.append(word[letter])
        if grand_hyphen_list[letter] == True:
            return_word.append(HYPHEN)

    return ''.join(return_word)


# For toggling message print during processing
def print_m(message, toggle, end='x'):

    if toggle == True:

        if end == '':
            print(message, end='')

        else:
            print(message)


# Shorthand
hw = weijters_hyphenate

