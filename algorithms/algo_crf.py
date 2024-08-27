import os
import chaine
from chaine import Model

# Establish model path, load
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'crf_model.chaine')
model_dutch = Model(model_path)

model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'eng_crf_model.chaine')
model_eng = Model(model_path)  

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
