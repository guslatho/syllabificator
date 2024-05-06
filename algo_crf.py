import os
import chaine
from chaine import Model

# This is for compiling the crf_model. Github does not allow filesize 25<mb
# so to remedy the original file was split into parts. Only runs the first
# time the application is run
current_directory = os.path.dirname(__file__)
file_path = os.path.join(current_directory, 'model_crf.chaine')
if os.path.exists(file_path) == False:
    print('Initializing Syllabificator...')
    print('CRF Model not detected. Compiling model_crf.chaine...')

    def join_files(output_file, *input_files):
        with open(output_file, 'wb') as outfile:
            for input_file in input_files:
                with open(input_file, 'rb') as infile:
                    outfile.write(infile.read())

    join_files('model_crf.chaine',
           'model_crf.chaine.part0',
           'model_crf.chaine.part1',
           'model_crf.chaine.part2')

    print('Model compilation successful!')
    print('(Note: The files model_crf.chaine.part0-2 in the current directory are no longer needed and can be safely deleted.)')

model = Model('model_crf.chaine')

def crf_hyphenate(word):

    # For storing all the observations of every letter of the word
    ttl = test_token_list = []

    # For every character in the word, look at possible substrings
    for char in range(len(word)):

        current_dict = {}
        current_dict['char'] = word[char]

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
            current_dict['2345'+value] = 1
        if char-3 >= 0 and char+1 < len(word):
            value = word[char-3:char+2]
            current_dict['3456'+value] = 1
        if char-2 >= 0 and char+2 < len(word):
            value = word[char-2:char+3]
            current_dict['3456'+value] = 1
        if char-1 >= 0 and char+3 < len(word):
            value = word[char-1:char+4]
            current_dict['4567'+value] = 1            
        if char+4 < len(word):
            value = word[char:char+5]
            current_dict['5678'+value] = 1
            
        ttl.append(current_dict)

    # Run the input word with different feature observations stored through the model
    hyphens = model.predict([ttl])[0]
    
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

    word_output = ''.join(word_output)

    return word_output
