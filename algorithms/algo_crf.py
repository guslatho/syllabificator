# Python implementation using Chaine of a model put forth in Trogkanis, N., & Elkan, C. (2010). Conditional random 
# fields for word hyphenation. In J. Hajič, S. Carberry, S. Clark, & J. Nivre (Eds.), Proceedings of the 48th Annual 
# Meeting of the Association for Computational Linguistics (pp. 366–374). Association for Computational Linguistics.

import os
import chaine
from chaine import Model

# This is for compiling the crf_model. Github does not allow filesize 50<mb
# so to remedy the original file was split into parts. Only runs the first
# time the application is run
current_directory = os.path.dirname(__file__)
file_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'crf_model.chaine')
file_path_eng = os.path.join(os.path.dirname(__file__), '..', 'models', 'eng_crf_model.chaine')
join_path = os.path.join(os.path.dirname(__file__), '..', 'models')

if (os.path.exists(file_path) == False) or (os.path.exists(file_path_eng) == False):
    print('CRF Model not detected. Compiling model_crf.chaine...')

    def join_files(output_file, *input_files):
        with open(output_file, 'wb') as outfile:
            for input_file in input_files:
                with open(input_file, 'rb') as infile:
                    outfile.write(infile.read())

    join_files(join_path+'\\crf_model.chaine',
           join_path+'\\model_crf.chaine.part0',
           join_path+'\\model_crf.chaine.part1',
           join_path+'\\model_crf.chaine.part2',
           join_path+'\\model_crf.chaine.part3',
           join_path+'\\model_crf.chaine.part4')

    join_files(join_path+'\\eng_crf_model.chaine',
           join_path+'\\eng_model_crf.chaine.part0',
           join_path+'\\eng_model_crf.chaine.part1')

    print('README.md')
    print('(Note: The files *.chaine.part0-4 in the current directory are no longer needed and can be deleted.)')


# Establish model path, load
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'crf_model.chaine')
model_dutch = Model(model_path)

model_path_eng = os.path.join(os.path.dirname(__file__), '..', 'models', 'eng_crf_model.chaine')
model_eng = Model(model_path_eng)  

def crf_syllabificate(input_word, language='nl'):

    # For storing all the observations of every letter of the word
    ttl = test_token_list = []

    # Characters are added to beginning and end of word and removed later
    word = '#!' + input_word + '%&'

    # For every character in the word, look at possible substrings
    for char in range(len(word)):

        current_dict = {}
        current_dict[str(len(word)-char)] = 1
        current_dict[str(word[char])] = 1

        # 2-window feature observations, i.e. 'g[ev]en' and 'ge[ve]n' for i=3
        if char-1 >= 0:
            value = word[char-1:char+1]
            current_dict['45'+value] = 1
        if char+1 < len(word):
            value = word[char:char+2]
            current_dict['56'+value] = 1

        # 3-window observations
        if char-2 >= 0:
            value = word[char-2:char+1]
            current_dict['345'+value] = 1
        if char-1 >= 0 and char+1 < len(word):
            value = word[char-1:char+2]
            current_dict['456'+value] = 1
        if char+2 < len(word):
            value = word[char:char+3]
            current_dict['567'+value] = 1

        # 4-window
        if char-3 >= 0:
            value = word[char-3:char+1]
            current_dict['2345'+value] = 1
        if char-2 >= 0 and char+1 < len(word):
            value = word[char-2:char+2]
            current_dict['3456'+value] = 1
        if char-1 >= 0 and char+2 < len(word):
            value = word[char-1:char+3]
            current_dict['4567'+value] = 1            
        if char+3 < len(word):
            value = word[char:char+4]
            current_dict['5678'+value] = 1

        # 5-window
        if char-4 >= 0:
            value = word[char-4:char+1]
            current_dict['12345'+value] = 1
        if char-3 >= 0 and char+1 < len(word):
            value = word[char-3:char+2]
            current_dict['23456'+value] = 1
        if char-2 >= 0 and char+2 < len(word):
            value = word[char-2:char+3]
            current_dict['34567'+value] = 1
        if char-1 >= 0 and char+3 < len(word):
            value = word[char-1:char+4]
            current_dict['45678'+value] = 1            
        if char+4 < len(word):
            value = word[char:char+5]
            current_dict['56789'+value] = 1

        # 6-window
        if char-5 >= 0:
            value = word[char-5:char+1]
            current_dict['012345'+value] = 1
        if char-4 >= 0 and char+1 < len(word):
            value = word[char-4:char+2]
            current_dict['123456'+value] = 1
        if char-3 >= 0 and char+2 < len(word):
            value = word[char-3:char+3]
            current_dict['234567'+value] = 1
        if char-2 >= 0 and char+3 < len(word):
            value = word[char-2:char+4]
            current_dict['345678'+value] = 1
        if char-1 >= 0 and char+3 < len(word):
            value = word[char-1:char+5]
            current_dict['456789'+value] = 1                        
        if char+5 < len(word):
            value = word[char:char+6]
            current_dict['56789x'+value] = 1
                    
        ttl.append(current_dict)

    ttl = [ttl]

    # Run the input word with different feature observations stored through the model
    if language=='nl':
        prediction = model_dutch.predict(ttl)
    if language=='eng':
        prediction = model_eng.predict(ttl)
    
    hyphens = prediction[0]
    word_output = []

    # Decode the output. '1' and '3' is followed by a hyphen, '0' and '2' aren't
    # Coding is:
    # 0: no hyphen follows the character, no hyphen precedes
    # 1: a hyphen follows, but no hyphen precedes
    # 2: a hyphen precedes, but no hyphen follows
    # 3: a hyphen precedes AND follows
    for letter in range(len(word)):
        if hyphens[letter] == '1' or hyphens[letter] == '3':
            word_output.append(word[letter]+'-')
        else:
            word_output.append(word[letter])

    # Return
    output_string = ''.join(word_output)
    output_string = output_string[2:-2]

    return output_string
