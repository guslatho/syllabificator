import MAIN_execute as Me
import pandas as pd

text = 'De nieuwsgierige man doorzocht de bibliotheek.'
word = 'supercalifragilisticexpialidocious'




# --- TEXT INPUT FOR DIRECT PROCESSING ---

# Hyphenate text: using no arguments employs standard library (if installed!)
print(Me.hyphenate_text(text))

# Select another algorithm with alg='b' for Brandth, alg='w' for Weijters
print(Me.hyphenate_text(text, alg='b'))
print(Me.hyphenate_text(text, alg='w'))

# For Weijters, put the w_size higher (max is 290000 for standard library)
# increases scope of word search.
print(Me.hyphenate_text(text, alg='w', w_size=200))



# --- WORD INPUT FOR PROCESSING --- 

# The subfunction hyphenate_word can also be used, though does not support
# non-alpha characters:
print(Me.hyphenate_word(word, alg='l', pattern=1))

# hyphenate_word uses the same arguments as hyphenate_text:
print(Me.hyphenate_word(word, alg='b'))
print(Me.hyphenate_word(word, alg='w', w_size=100))




# --- HYPHENATION SUCCESS RATE ANALYZE FUNCTION --- 

# To analyze datasets, two functions can be run. The first takes
# a list of hyphenated words and runs the available algorithms against it:

sample_set = pd.read_csv('set_loan_hyphenated_sample.csv', header=None)
sample_set = sample_set[0]

# Input a seroes set into run_all. It will prompt dataset name.
# Order of algorithm is as follows (enter these for each dataset):
# Algorithm 1: Brandt
# Algorithm 2: Liang
# Algorithm 3: Wetijers
Me.run_all(sample_set, print_info=True)


# If you already have a set with hyphenated solutions and want to run them,
# you can use the run_sets function. Order of entry for arguments is:
# Reference set (list of words of correct hyphenation solutions)
# Testset 1 (list of words 1 you want to compare against reference set)
# Testset 2 (list of words 2 you want to compare against reference set)
# Testset 3 etc.

sample_set = pd.read_csv('set_loan_hyphenated_sample.csv', header=None)
sample_set = sample_set[0]

chat_set = pd.read_csv('solutions_loan_chat_sample.csv', header=None)
chat_set = chat_set[0]

Me.run_sets(sample_set, chat_set)



