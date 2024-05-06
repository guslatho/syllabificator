import pyphen

pyphen.language_fallback('nl_NL_variant1')

# Loads different libraries

# Standard pattern library (old tex-96 equivalent)
dic_standard = pyphen.Pyphen(lang='nl_NL', left=2, right=2)

# Custom pattern set based on 1/1 margins. Optimal solution
dic_cust_pattern = pyphen.Pyphen(lang='_cus_pattern', left=1, right=2)

def liang_hyphenate(word, library=2):

    if library == 1:
        return dic_standard.inserted(word)

    if library == 2:
        return dic_cust_pattern.inserted(word)

    
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
