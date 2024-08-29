# Syllabificator

Syllabificator is an open-source tool for splitting **words** into **syl-la-bles** (syllabify). The project aims to offer easy access to high-quality syllabification algorithms for Dutch and English.

## Algorithms (CRF/NN)

Two algorithms which match the best performance described in the literature are included:

* **Conditional Random Field**. A 2010 model by Trogkanis and Elkan, replicated using Chaine (CRF package for Python). Trogkanis and Elkan report a word accuracy of 99.51% for Dutch dictionary words and 96.33% for English dictionary words, current replication scores 99.45% for Dutch dictionary words.
* **Neural Net model**. A new approach that uses deep learning to analyze subword patterns (presented at CLIN 34). Comparisons shows improvements in comparison with the CRF model, especially on complex word forms (peak recorded accuracy of 99.57% on Dutch dictionary words).

## Algorithm Overview
Below table displays all five models which can be run:

| Algorithm   | Type          | Dutch | English | Origin |
|-------------|---------------|-------|---------|--------|
| Brandt      | Linguistic    | V     | x       | Brandt Corstius, H. (1970). Exercises in computational linguistics |
| Liang       | Algorithmic   | V     | x       | Liang, F. M. (1983). Word hy-phen-a-tion by com-put-er |
| Weijters    | Lookup-based  | V     | x       | Weijters, A. J. M. M. (1991). A SIMPLE LOOK-UP PROCEDURE SUPERIOR TO NETTALK? |
| CRF         | Conditional Random Field (Linear Chain)  | V     | V       |  Trogkanis, N., & Elkan, C. (2010). Conditional random fields for word hyphenation |
| NN          | Deep learning (Neural Net)    | V     | V       | (Newly added) |

* Note that Syllabificator divides words according to **phonetic pronounciation**, which differs from word dividing based on **spelling conventions**.
See [this page](https://new.reddit.com/r/asklinguistics/comments/1elahiq/what_is_the_point_of_hyphenations_in_dictionaries/) for a brief discussion.

## Algorithm Performance

For Dutch, performance of the algorithms was tested on three datasets ([CELEX](https://catalog.ldc.upenn.edu/LDC96L14), loan words derived from [de Sijs](https://www.dbnl.org/tekst/sijs002groo01_01/), pseudowords derived from [CHOREC](https://taalmaterialen.ivdnt.org/download/tstc-chorec-spraakcorpus/)) to evaluate algorithm effectiveness. Below displayed are the word error rate for each set for each algorithm:

![performance_comparison](https://github.com/user-attachments/assets/ae5ef9e5-7be5-4f34-a305-c691a4f3db2c)

For English, the recorded word error rates on a 99.5/0.5% split are as follows:

| Algorithm   | Word Error Rate % |
|-------------|-------------------|
| CRF         | 3.64%            |
| NN          | 1.21%            |

See end of page for short performance comparison applied to an actual document.

# Usage

Syllabificator requires the following dependencies:
* Pandas
* Numpy
* Chaine
* Python 3.11 environment with tensorflow 2.13 for the Neural Net.

Use the requirements.txt to copy the original virtual environment (see end of page).

## Syllabifying words

The most general function syllabifies a string of text into an output with individual syllables. It can be run from the main module,
`main.py`:

```python
>>> text = 'De nieuwsgierige man doorzocht de bibliotheek.'
>>> syllabificate_text(text)
'De nieuws-gie-ri-ge man door-zocht de bi-bli-o-theek.'
```

The `syllabificate_text` function supports non-alpha characters, however does not currently take into consideration special characters
when syllabifying (e.g., `é`).

A more specific function employed by `syllabificate_text` is `syllabificate_word`, which can also be used individually. It only supports
lower-case letter input, meaning any other input is better suited to use the `syllabificate_text` function.

```python
>>> word = 'barracuda'
>>> syllabificate_word(word)
'bar-ra-cu-da'
```
Without any additional parameters, `syllabificate_text` and `syllabificate_word` will automatically employ the quickest algorithm (CRF). 
Other algorithms can be manually selected by changing the `alg` parameter:

```python
>>> word = 'chocoladetaart'
>>> syllabificate_word(word, alg='b')
'cho-co-la-de-taart'
```
To syllabify English words, use the language='eng' parameter:

```python
>>> word = 'christmas'
>>> syllabificate_word(word, language='eng')
'christ-mas'
```
```python
>>> word = 'jellybean'
>>> syllabificate_word(word, alg='n', language='eng')
'jel-ly-bean'
```

To call different algorithms, the following commands can be used for the `hyphenate_text` and `hyphenate_word` functions:
| Algorithm   | Command          | Note |
|-------------|---------------|--------|
| Brandt      | `alg='b'`    | (Not available for English) |
| Liang       | `alg='l'`   | (Not available for English) |
| Weijters    | `alg='w'`  | (Not available for English) |
| CRF         | `alg='c'`  | |
| Neural Net  | `alg='n'`  | |


## Performing Analyses

Syllabificator supports analyses comparing the output of different algorithms versus a correct solution. It displays a number of metrics, e.g., 
false positives, overall error rate and more. The `run_all` function simply takes an input list of correctly syllabized words (as a pandas series) 
and applies the different algorithms to them. Output is a table with the different relevant metrics.

```python
>>> sample_set = pd.read_csv('set_loan_hyphenated.csv', header=None)  # .csv containing hyphenated words seperate by break
>>> sample_set = sample_set[0]  # Cast as series
>>> Me.run_all(sample_set, print_info=True)
'Please input name of dataset 1 (for display purposes):'
>>> Brandt
'Please input name of dataset 2 (for display purposes):'
>>> Liang
'Please input name of dataset 3 (for display purposes):'
>>> CRF
'Please input name of dataset 4 (for display purposes):'
>>> Weijters
'Please input name of dataset 5 (for display purposes):'
>>> NN
'Processing...'
'           TP  FP  TN  FN  owe  swe    %ower   %swer   %oler   %sler'
'CORRECT    98   0  462   0    0    0   0.000   0.000   0.000   0.000'
'NO_HYPHEN   0   0  462  98   59    0  59.596   0.000  17.500   0.000'
'Brandt     97   2  460   1    2    2   2.020   2.020   0.536   0.357'
'Liang      93   9  453   5   10    9  10.101   9.091   2.500   1.607'
'CRF        97   4  458   1    4    4   4.040   4.040   0.893   0.714'
'Weijters   63  71  391  35   61   52  61.616  52.525  18.929  12.679'
'NN         96   3  459   2    3    3   3.030   3.030   0.893   0.536'
```
The second analyses function `run_sets` performs identically, however takes lists of first a correctly hyphenated
reference set followed by x amounts of lists to check against. All lists are input as a pandas series with equal length:

```python
>>> sample_set = pd.read_csv('set_loan_hyphenated_sample.csv', header=None) 
>>> sample_set = sample_set[0]
>>> chat_set = pd.read_csv('solutions_loan_chat_sample.csv', header=None)  
>>> chat_set = chat_set[0]  # List of hyphenation solutions generated by an internal or external algorithm
>>> Me.run_sets(sample_set, chat_set)
'Please input name of dataset 1 (for display purposes):'
>>> Algo-x
'           TP  FP  TN  FN  owe  swe    %ower   %swer   %oler  %sler'
'CORRECT    18   0  56   0    0    0    0.000   0.000   0.000  0.000'
'NO_HYPHEN   0   0  56  18    9    0  100.000   0.000  24.324  0.000'
'Algo-x     16   1  55   2    2    1   22.222  11.111   4.054  1.351'
```
### Sample script

The default directory contains a sample script executing the above functions on different sample libraries. It is listed
as `sample_script.py` in the main directory

## Misc

The deep learning model was created using a custom CRF addon only compatible with an older version of Tensorflow. To run it, the requirements.txt
file can be used to recreate the original environment (note that it requires a Python==3.11 environment).

Alternatively, the recreate the environment in full from scratch, the following steps can be performed manually:

* Create a new environment with `python=3.11`
* Install `numpy==1.24.3` and `pandas==2.2.2`
* Install `tensorflow==2.13.0`
* Install `tensorflow-addons==0.22.0`
* Install `keras_crf==0.3.0`
* Install `chaine==3.12.1`

### To-do

| Done   | Description |
|-------------|-------------------|
|  | Add hyphenation support (syllable dividing according to grammar rules) |
|  | Hyperparameter tuning for english NN |
|  | Fix NN processing from individual word to batch (increase computation speed) |
|  | Add Liang/Weijter's algorithm for English |
|  | Add syllable counting |
|  | Add support for NN for words longer than 34 character (Dutch) / 22 characters (English) |

### Sample Benchmark: First chapter of Harry Potter

Below is a comparison of outputs of the 3 best-performing algorithms (Liang, CRF, Neural). Applied to the first chapter of Harry Potter, they only differed
on output for 13 words:

```python
                         CRF                   LIANG                      NN
207   on-Duf-fe-ling-ach-tig  on-Duf-fel-ing-ach-tig  on-Duf-fe-ling-ach-tig
600                   fi-le,                  fi-le,                   file,
658                  zoot-je               zo-o-t-je                 zoot-je
965                   do-nut                  don-ut                  do-nut
1300                 blij-e,                  blije,                 blij-e,
1301                  blij-e                   blije                  blij-e
1441              ‘Ks-ssjt!’              ‘Kss-sjt!’               ‘Ksssjt!’
1575                mee-stal                meest-al                meest-al
1607          slaap-pa-troon         sla-ap-pa-troon          slaap-pa-troon
1720                   lui-e                    luie                   lui-e
1766             Pe-tu-ni-a,              Pe-tu-nia,             Pe-tu-ni-a,
2118              Pe-tu-ni-a               Pe-tu-nia              Pe-tu-ni-a
2323      bril-len-glaas-jes     bril-len-g-laas-jes      bril-len-glaas-jes
```

Note that NN had the highest success rate in this instance, followed by CRF and Liang.

For the English language, output on English first chapter is as follows:

```python
                  CRF               NN
117           Dud-ley          Du-dley
202   un-Durs-ley-ish  un-Dur-sley-ish
536         coul-dn’t         couldn’t
683           cou-ple          coup-le
1118         Ha-rold.         Har-old.
1261      pas-sers-by      pass-ers-by
1442      be-hav-ior?     be-hav-i-or?
1600       Mc-Guf-fin        McGuf-fin
1901        Dud-ley’s        Du-dley’s
2590  Mc-Gon-a-gall.”  McG-on-a-gall.”
2691   Mc-Gon-a-gall.   McG-on-a-gall.
2714    Mc-Gon-a-gall    McG-on-a-gall
3064   Mc-Gon-a-gall,   McG-on-a-gall,
3350  Mc-Gon-a-gall’s  McG-on-a-gall’s
3373       coul-dn’t.        couldn’t.
3551       “Ha-grid’s       “Hag-rid’s
3890          Ha-grid          Hag-rid
4083       “Ha-grid,”       “Hag-rid,”
4114          Sir-ius         Sir-i-us
4221       “Coul-dn’t        “Couldn’t
4292         Ha-grid.         Hag-rid.
4334         Ha-grid,         Hag-rid,
4443          min-ute          mi-nute
4455        Ha-grid’s        Hag-rid’s
4542             rose            ro-se
4559  Mc-Gon-a-gall,”  McG-on-a-gall,”
4778         Dud-ley.         Du-dley.
```
