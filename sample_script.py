import main as Me
import pandas as pd

# Sample words for syllabification
word_dutch = 'superformiweldigeindefantakolosachtig'
word_eng = 'supercalifragilisticexpialidocious'

# Sample texts for syllabification
text_dutch = '''In de Ligusterlaan, op nummer 4, woonden meneer en mevrouw Duffeling.
Ze waren er trots op dat ze doodnormaal waren en als er ooit mensen waren geweest
van wie je zou denken dat ze nooit bij iets vreemds of geheimzinnigs betrokken
zouden raken waren zij het wel, want voor dat soort onzin hadden ze geen tijd.

Meneer Duffeling was directeur van Drillings, een boormachinefabriek. Hij was groot
en gezet en had bijna geen nek, maar wel een enorme snor. Mevrouw Duffeling was
blond en mager en haar nek was twee keer zo lang als normaal, wat goed van pas
kwam omdat ze vaak over de schutting gluurde om de buren te bespioneren. De
Duffelingen hadden een zoontje, Dirk, en ze wisten zeker dat er nog nooit zo’n
fantastische baby was geweest.

De Duffelingen hadden alles wat hun hartje begeerde, maar ze hadden ook een geheim
en hun grootste angst was dat dat ontdekt zou worden. Ze zouden door de grond
zakken van schaamte als iemand hoorde van de Potters. Mevrouw Potter was de
zus van mevrouw Duffeling, maar ze hadden elkaar al jaren niet gezien; mevrouw
Duffeling deed zelfs alsof ze helemaal geen familie had, omdat haar zus en haar
nietsnut van een man zo on-Duffelingachtig waren als maar zijn kon. Bij de
gedachte aan wat de buren zouden zeggen als de Potters ooit op bezoek kwamen,
knepen de billen van de Duffelingen samen. De Duffelingen wisten dat de Potters
ook een zoontje hadden, maar dat hadden ze nog nooit gezien. Dat zoontje was
zelfs een extra reden om de Potters buiten de deur te houden; ze wilden niet dat
Dirk met zo’n kind om zou gaan.
'''.replace('\n', ' ')

text_english = '''Mr. and Mrs. Dursley, of number four, Privet Drive, were
proud to say that they were perfectly normal, thank you very much. They were the
last people you’d expect to be involved in anything strange or mysterious, because
they just didn’t hold with such nonsense.

Mr. Dursley was the director of a firm called Grunnings, which made drills. He was
a big, beefy man with hardly any neck, although he did have a very large mustache.
Mrs. Dursley was thin and blonde and had nearly twice the usual amount of neck,
which came in very useful as she spent so much of her time craning over
garden fences, spying on the neighbors. The Dursleys had a small son called Dudley
and in their opinion there was no finer boy anywhere. The Dursleys had everything
they wanted, but they also had a secret, and their greatest fear was that somebody
would discover it.

They didn’t think they could bear it if anyone found out about the Potters. Mrs.
Potter was Mrs. Dursley’s sister, but they hadn’t met for several years; in fact,
Mrs. Dursley pretended she didn’t have a sister, because her sister and her
good-for-nothing husband were as unDursleyish as it was possible to be. The
Dursleys shuddered to think what the neighbors would say if the Potters arrived
in the street. The Dursleys knew that the Potters had a small son, too, but
they had never even seen him. This boy was another good reason for keeping the
Potters away; they didn’t want Dudley mixing with a child like that. 
'''.replace('\n', ' ')

# --- SYLLABIFICATING WORDS ---
print("\n" + "-" * 50)
print('DUTCH WORD SAMPLE:')
print('CRF   : ' + Me.syllabificate_word(word_dutch))
print('Liang : ' + Me.syllabificate_word(word_dutch, alg='l'))
print('(**Note that the NN supports up to 34 characters in a word:**)')
print('NN    : ' + Me.syllabificate_word(word_dutch[:34], alg='n'))

print("\n" + "-" * 50)
print('ENGLISH WORD SAMPLE:')
print('CRF   : ' + Me.syllabificate_word(word_eng, language='eng'))
print('(**The English NN supports up to 22 characters:**)')
print('NN    : ' + Me.syllabificate_word(word_eng[:22], alg='n', language='eng'))

print("\n" + "-" * 50)
print('DUTCH TEXT SAMPLE (NN):')
print(Me.syllabificate_text(text_dutch, alg='n'))

print("\n" + "-" * 50)
print('ENGLISH TEXT SAMPLE (CRF):')
print(Me.syllabificate_text(text_english, language='eng'))

# --- HYPHENATION SUCCESS RATE ANALYZE FUNCTION --- 

# To analyze datasets, two functions can be run. The first takes
# a list of hyphenated words and runs the available algorithms against it:

sample_set = pd.read_csv('data/set_loan_hyphenated_sample.csv', header=None)
sample_set = sample_set[0]  # Convert to series

# Input a seroes set into run_all. It will prompt dataset name.
# Order of algorithm is as follows (enter these for each dataset):
# Algorithm 1: Brandt
# Algorithm 2: Liang
# Algorithm 3: CRF
# Algorithm 4: Wetijers
print("\nRunning analysis on sample set using run_all:")
print("\n[NOTE: DEFAULT INPUT NAME FOR DATASET1 = Brandt, 2 = Liang etc:]")
Me.run_all(sample_set)

# If you already have a set with hyphenated solutions and want to run them,
# you can use the run_sets function. Order of entry for arguments is:
# Reference set (list of words of correct hyphenation solutions)
# Testset 1 (list of words 1 you want to compare against reference set)
# Testset 2 (list of words 2 you want to compare against reference set)
# Testset 3 etc.

print("\nRunning comparison between sample set and chat set using run_sets:")
print("\n[NOTE: Name for dataset 1 would be Chat-GPT in this case since syllabifications are Chat-GPT generated]")
sample_set = pd.read_csv('data/set_loan_hyphenated_sample.csv', header=None)
sample_set = sample_set[0]

chat_set = pd.read_csv('data/solutions_loan_chat_sample.csv', header=None)
chat_set = chat_set[0]

Me.run_sets(sample_set, chat_set)

print("\nAnalysis completed successfully.")
