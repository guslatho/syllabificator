import time
import sys, os
import pandas as pd

# Compression Matrix
compression_matrix = ['y', 'oi', 'oui', 'aai', 'ay', 'ooy', 'aau', 'u', 'aa',
                      'i', 'ee', 'ae', 'ij', 'oeu', 'c', 'h', 'ai', 'j', 'oe',
                      'aay', 'oy', 'ei', 'oei', 'oey', 'oo', 'ou', 'au', 'ui',
                      'ie', 'q', 'a', 'e', 'ooi', 'qu', 'uy', 'o', 'ey', 'eeu',
                      'ieu', 'eu', 'eui', 'ch', 'uu']

# Vowels
vowels = {3:['oui', 'aai', 'ooy', 'aau', 'oeu', 'aay', 'oei', 'oey', 'ooi', 'eeu',
             'ieu', 'eui'],
          2:['oi', 'ay', 'aa', 'ee', 'ae', 'ij', 'ai', 'oe', 'oy', 'ei', 'oo', 'ou',
             'au', 'ui', 'ie', 'uy', 'ey', 'eu', 'uu'],
          1:['u', 'i', 'a', 'e', 'o' ,'y']}

consonants = ['b', 'c', 'd', 'f', 'g', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's',
              't', 'v', 'w', 'x', 'z']

# 'aai'-group
aai_group = ['aai', 'aay', 'oei', 'oey', 'ooi']

# 'aa'-group
aa_group = ['uu', 'aa', 'ee', 'oo']


# Suffixes and prefixes 
suffixes = ["aard", "heid", "laan", "lijk", "loos", "wijs", "ren", "rijk",
            "land", "ling", "ring", "put"]

prefixes = {5:["aarts", "voort", "hoofd", "noord", "groot"],
            4:["daar", "hier", "voor", "maat", "zuid"],
            3:["der", "ven", "ver", "her", "wan", "sub", "dis", "ont",
               "aan", "oor", "van", "nog", "hof", "jet", "als", "oer"],
            2:["in", "on",  "er", "af", "ab"]}

# List of pronouncable pairs (C2 in Brand Corstius)
pronouncable_pairs = c_two = ['pl', 'pr', 'tr', 'chr', 'bl', 'br', 'cl', 'cr', 'dr',
                      'fl', 'gr', 'kl', 'kr', 'kw', 'sc', 'sch', 'th', 'vl',
                      'wr', 'zw', 'fr', 'st', 'sp']

# Pronouncable triplets (C3)
pronouncable_triples = c_three = ['spl', 'spr', 'str', 'schr']            

# For cleaning up sentence output
non_alpha = [' ', '?', '.', ',']

# Main function, splits words into syllables following Brandt Corstius
        
def brandt_syllabificate(word, print_toggle=False):
    processing_word = word
    word_output = []
    
    # If there are suffixes, remove these first
    suffixed_word = cut_suffix(word)
    if len(suffixed_word) > 1:
        print_m('Suffixes encountered in word! The following suffixes were found: '
              + str(suffixed_word[1:]), print_toggle)
        processing_word = suffixed_word[0]

    # Word compression. Split word into characters (e.g. 'kaas', -> 'k' 'aa' 's')
    split_word = vowel_split(processing_word)
    vowel_pos = vowel_positions(split_word)
    loops = len(vowel_pos)-1
    if loops < 1:
        print_m('Finished! No syllables to process (besides possible '
              + 'suffixes. Returning output word', print_toggle)
        return ''.join(vowel_split('-'.join(suffixed_word)))

    # Print summary
    print_m('Characters to be processed (excluding prefixes/suffixes): \n- '
          + str(split_word), print_toggle)
    print_m('Total syllable count (excluding prefixes/suffixes): \n- '
          + str(loops+1), print_toggle)

    # Loop to check each syllable pair
    starting_point = 0 #  Starting point for each syllable that is being processed    
    for pair in range(loops):

        first_vowel = vowel_pos[pair] - starting_point
        second_vowel = vowel_pos[pair+1] - starting_point

        print_m('Currently processing word-section number ' + str(pair+1) +
              '. Section analyzed is \n- ' + str(split_word[starting_point:]), print_toggle)
        
        # 'aai'-exception: if 1st vowel is in aai-groep, hyphenate on the spot
        if split_word[first_vowel+starting_point] in aai_group:

            processed = split_word[starting_point:first_vowel+1+starting_point] + ['-']
            word_output = word_output + processed
            print_m('aai-exception detected.', print_toggle, end='')

        # First, check to see if VV combination, if so process
        elif second_vowel - first_vowel == 1:
            vowel_two_end = (pair+1 == loops+1 and pair+1 == len(split_word))
            if vowel_pos[pair+1] == len(split_word)-1: #  If 2nd vowel at end word
                vowel_two_end = True
            else:
                vowel_two_end = False
            processed = process_two_length(split_word[starting_point:],
                                           first_vowel,
                                           second_vowel,
                                           vowel_two_end)
            print_m('VV combination detected!', print_toggle, end='')
            word_output = word_output + processed

        # After that, check for VCV combination if present
        elif second_vowel - first_vowel == 2:
            vowel_two_end = ((pair+1 == loops)
                              and (split_word[vowel_pos[pair+1]] == split_word[-1]))

            print_m(vowel_two_end, print_toggle)

            processed = process_three_length(split_word[starting_point:],
                                             first_vowel,
                                             second_vowel,
                                             vowel_two_end,
                                             split_word[starting_point-1]) 
            print_m('VCV combination detected!', print_toggle, end='')
            word_output = word_output + processed

        # Check for 5-length+ combinations (VCCCV, VCCCCV, e.g. kasplant)
        elif ((second_vowel-first_vowel > 4 and
               ''.join(split_word[second_vowel-4:second_vowel]) == 'schr') or
              (second_vowel-first_vowel > 3 and
               ''.join(split_word[second_vowel-3:second_vowel]) in c_three)):
            processed = process_five_length(split_word[starting_point:],
                                            first_vowel,
                                            second_vowel,
                                            5)
            print_m('VCCCV combination detected!', print_toggle, end='')
            word_output = word_output + processed

        # Misc combinations. Will either be VCCCV or VCCV
        else:
            processed = process_misc_length(split_word[starting_point:],
                                            first_vowel,
                                            second_vowel)
            print_m('VCC(C)V combination detected!', print_toggle, end='')
            word_output = word_output + processed

        # Remove all instances of hyphen from the list, for checking start point
        cleaned_list = [char for char in word_output if char != '-']
                
        # Set new starting point from which to process after each syllable
        starting_point = len(cleaned_list)

    # Add the remainder tail of word    
    word_output = word_output + split_word[starting_point:]

    # Add any suffixes cut in the beginning 
    if len(suffixed_word) > 1:
        word_output = word_output + ['-'] + ['-'.join(suffixed_word[1:])]

    return ''.join(word_output)

# For toggling message print during processing
def print_m(message, toggle, end='x'):

    if toggle == True:

        if end == '':
            print(message, end='')

        else:
            print(message)

# Returns vowel positions from a list e.g. ['k','o','p','e','n'] results in 1 and 3
def vowel_positions(split_word):
    count = 0
    position_list = []
    for character in split_word:
        if character in (vowels[1] + vowels[2] + vowels[3]):
            position_list.append(count)
        count += 1
    return position_list

# Cut off suffixes at end of the word. Repeat until no suffix left
def cut_suffix(word):
    word_end = len(word)
    return_word = []
    while True:
        if word[word_end-4:word_end] in suffixes:
            return_word.insert(0,word[word_end-4:word_end])
            word_end -= 4        
        elif word[word_end-3:word_end] == 'ren':
            return_word.insert(0,word[word_end-3:word_end])
            word_end -= 3
        else:
            return_word.insert(0, word[0:word_end])
            return return_word

# Cut off prefixes until none left. If input is a split word, output as split word
def cut_prefix(word, split=False):
    word_begin = 0
    return_word = []
    check_length = 5
    if split == True:
        word = ''.join(word)
    while True:
        # Check for 5-length prefix, then for 4, 3 etc.
        if word[word_begin:word_begin+check_length] in prefixes[check_length]:
            return_word.append(word[word_begin:word_begin+check_length])
            word_begin += check_length
            check_length = 5
        elif check_length > 2:
            check_length -= 1
        else:
            return_word.append(word[word_begin:])
            #If word is two times prefix (e.g. "erven") remove empty '' added
            if return_word[-1] == '':
                return_word = return_word[:-1]
            if split == True:
                # Note: in case of split word, only return 1st syllable
                return_word = vowel_split(return_word[0]) + ['-']
            return return_word
            
# Count number of syllables. Set split to True if inputting already split word
def count_syllables(word,split=False):
    syllable_count = 0
    if split==False:
        word = vowel_split(word)
    for character in word:
        if character in vowels[1] + vowels[2] + vowels[3]:
            syllable_count += 1
    return syllable_count

# Compress word, meaning split character into consonant + vowel combinations
def vowel_split(word):
    letter_position = 0  
    word_length = len(word)
    word_split = []  # Output list (word as seperated characters)
    while True:
        if letter_position > word_length-1: # Return word if done
            return word_split
        # If consonant, continue
        if word[letter_position] in (consonants + ["'","y","h","j","-"]):
            word_split.append(word[letter_position])
            letter_position += 1
        # If vowel, perform compression if possible (e.g. 'e''e' -> 'ee')
        elif word[letter_position] in vowels[1]:
            if word[letter_position:letter_position+3] in vowels[3]:
                word_split.append(word[letter_position:letter_position+3])
                letter_position += 3
            elif word[letter_position:letter_position+2] in vowels[2]:
                word_split.append(word[letter_position:letter_position+2])
                letter_position += 2
            else:
                word_split.append(word[letter_position])
                letter_position += 1
        else:
            print(str(word[letter_position]))
            print('Error encountered during splitting of vowels: word ' +
                  'contains invalid characters')
            break

# Following functions are used for syllable processing
    
# For processing 2-length vowel combinations (VV)
# (remove second_word_end, not used)
def process_two_length(char_list,
                       first_vowel,
                       second_vowel,
                       second_word_end):
    # There's only one exception for VV vowel pairs; in case of -eau
    vowel_pair = char_list[first_vowel:second_vowel+1]
    if ''.join(vowel_pair) == 'eau':
        return char_list[0:first_vowel] + ['e', 'au']
    else:
        return char_list[0:first_vowel+1] + ['-']


# For processing 3-length vowel combinations (VCV)
def process_three_length(char_list,
                         first_vowel,
                         second_vowel,
                         second_v_word_end,
                         min_one_char):
    # First exception, if the consonant is an 'x' do not hyphenate (e.g. 'exa-men')
    if char_list[first_vowel+1] == 'x':
        return char_list[:first_vowel+1]
    # Second, in case of 'aa'-group there's another exception (e.g. 'raam-glas')
    if char_list[first_vowel] in aa_group and first_vowel > 0:
        front = ''.join(char_list[0:2])
        # However, if part begins with mee/zee/wee, keep intact (e.g. 'zee-slag')
        if front in ['mee', 'wee', 'zee']:
            return char_list[:2] + ['-']
        elif second_v_word_end == False:
            return char_list[:second_vowel] + ['-']
    # Third, exception for 'on'-woorden (e.g. 'on-echt'). Do not apply if 'io-n'
    # (fix so that 'i' at end of sentence doesn't carry over)
    if ''.join(char_list[:2]) == 'on' and min_one_char != 'i':
        return char_list[:2] + ['-']
    # Cut off prefix 
    try_prefix_cut = cut_prefix(char_list, True)
    if second_v_word_end == False and (len(try_prefix_cut) != len(char_list)+1):
        return try_prefix_cut
    # Finally, cut regularly CVC if none of above conditions are triggered
    return char_list[:first_vowel+1] + ['-']
    
# For processing 5-length vowel combinations or longer (VCCCV, VCCCCV)
def process_five_length(char_list,
                        first_vowel,
                        second_vowel,
                        word_end):
    # '-ustr-' exception, for example 'indus-trie' instead of 'indus-trie'
    if char_list[first_vowel] == 'u':
        return char_list[:first_vowel+2] + ['-']
    # >>? 'Spr' exception (nog doen, o=2 en word end>16). Deze vaag
    # >> Cut prefix nog doen. Simpelweg kijken of prefix er is, zoja wegdoen
    try_prefix_cut = cut_prefix(char_list, True)
    if len(try_prefix_cut) != len(char_list)+1:
        return try_prefix_cut 
    # 'aa' group exception. If not 'schr' cut +1 after vowel (e.g., 'kaas-plank)
    if char_list[first_vowel] in aa_group:
        if char_list[first_vowel+1:second_vowel] != 'schr':
            return char_list[:first_vowel+2] + ['-']
    # If none of the above, default V-CCCV out, with exception of 'schr'
    if (second_vowel - first_vowel > 4 and
        ''.join(char_list[second_vowel-4:second_vowel]) == 'schr'):
        return char_list[:second_vowel-4] + ['-']
    return char_list[:first_vowel+1] + ['-']

# For processing any vowel combination not flagged by previous (VCCCV or VCCV)
def process_misc_length(char_list,
                        first_vowel,
                        second_vowel):
    # "dummy" badly coded but works, it's for compensating for 'sch' in C2. Rewrite?
    dummy = 0
    if (''.join(char_list[second_vowel-2:second_vowel]) in c_two or
        ''.join(char_list[second_vowel-3:second_vowel]) in c_two):
        if ''.join(char_list[second_vowel-3:second_vowel]) in c_two:
            dummy = 1
        # 'aa' group exception.
        if (char_list[first_vowel] in aa_group) and (second_vowel-first_vowel == 3):
            return char_list[:first_vowel+2-dummy] + ['-']
        # Prefix cut if necessary
        try_prefix_cut = cut_prefix(char_list, True)
        if len(try_prefix_cut) != len(char_list)+1:
            return try_prefix_cut 
        # 'fr' 'st' 'sp' handling. If following consonant, split
        if ''.join(char_list[first_vowel+1:second_vowel]) in ['fr', 'st', 'sp']:
            # 'toestand' exception
            if  (second_vowel-first_vowel == 3 and not
                 (''.join(char_list[first_vowel+1:second_vowel]) == 'st' and
                 ''.join(char_list[second_vowel:second_vowel+3]) == 'and')):
                return char_list[:first_vowel+2-dummy] + ['-']
        # 'sc' exception: if sc follows another consonant, split between these
        if (''.join(char_list[second_vowel-2:second_vowel]) == 'sc' and
            char_list[second_vowel-3] in consonants):
            return char_list[:second_vowel-1-dummy] + ['-']
        # Unclear exception? Not mentioned in text but present in code
        if (second_vowel-first_vowel == 3 and
           ''.join(char_list[first_vowel+1:second_vowel]) == 'op'):
            return char_list[:second_vowel-2-dummy] + ['-']
        # Default: cut V-CCV
        return char_list[:second_vowel-2-dummy] + ['-']
    
    ## 'ngs' exception: if ngs followed by vowel, cut ngs- (e.g. 'konings-onthaal')
    if (''.join(char_list[first_vowel+1:first_vowel+4]) == 'ngs'
        and char_list[first_vowel+4] in vowels[1]+vowels[2]+vowels[3]):
        return char_list[:first_vowel+4] + ['-']
    # Prefix cut in case of non-C2/C3 try
    try_prefix_cut = cut_prefix(char_list, True)
    if len(try_prefix_cut) != len(char_list)+1:
        return try_prefix_cut 
    return char_list[:second_vowel-1-dummy] + ['-']
         


