import pyphen

pyphen.language_fallback('nl_NL_variant1')

# Loads different libraries

# Standard pattern library (old tex-96 equivalent)
dic_standard = pyphen.Pyphen(lang='nl_NL', left=2, right=2)

# Trogkanis pattern library replicated, right/left margins set at 2/3
dic_cust_one = pyphen.Pyphen(lang='_cus', left=2, right=3)

# Trogkanis pattern  library replicated, right/left margins set at 1/1
dic_cust_two = pyphen.Pyphen(lang='_cus', left=1, right=1)

# Custom pattern set based on 1/1 margins. Optimal solution
dic_cust_three = pyphen.Pyphen(lang='_cus_twee', left=1, right=2)

def liang_hyphenate(word, library=4):

    if library == 1:
        return dic_standard.inserted(word)

    if library == 2:
        return dic_cust_one.inserted(word)

    if library == 3:
        return dic_cust_two.inserted(word)

    if library == 4:
        return dic_cust_three.inserted(word)
    
# Possible word list for testing
wordlist = ['abaci',
            'abacus',
            'abattoir',
            'abele',
            'abeel',
            'gebutste',
            'nagels',
            'edelgas',
            'edelgermaan',
            'educt',
            'egale',
            'emittent',
            'eczeem',
            'eczema',
            'echten']
