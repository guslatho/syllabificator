# Syllabificator

Library and tool for syllabifying Dutch/English words and comparing output from different syllabification algorithms.

## General
### Description

Syllabificator is a tool for syllabifying words, meaning to split **words** into **pho-ne-tic** **com-pli-ant** **syl-la-bles**. It works
by directly employing algorithms from external libraries (like Pyphen) supplemented with implementations of algorithms manually coded.
There are currently five different algorithm that the tool supports:

| Algorithm   | Type          | Dutch | English | Origin |
|-------------|---------------|-------|---------|--------|
| Brandt      | Linguistic    | V     | x       | Brandt Corstius, H. (1970). Exercises in computational linguistics |
| Liang       | Algorithmic   | V     | x       | Liang, F. M. (1983). Word hy-phen-a-tion by com-put-er |
| Weijters    | Lookup-based  | V     | x       | Weijters, A. J. M. M. (1991). A SIMPLE LOOK-UP PROCEDURE SUPERIOR TO NETTALK? |
| CRF         | Conditional Random Field (Linear Chain)  | V     | V       |  Trogkanis, N., & Elkan, C. (2010). Conditional random fields for word hyphenation |
| NN          | Deep learning (Neural Net)    | V     | V       | (Newly added) |

* **!Note!** Syllabificator divides words according to **phonetic pronounciation**, which differs from word dividing based on **spelling conventions**.
See [this page](https://new.reddit.com/r/asklinguistics/comments/1elahiq/what_is_the_point_of_hyphenations_in_dictionaries/) for a brief discussion on the differences.

### Algorithm Performance

For Dutch, performance of the algorithms was tested on three datasets to evaluate algorithm effectiveness. Below displayed are the word error rate for each set for each algorithm:

![performance_comparison](https://github.com/user-attachments/assets/904c47ff-ebf8-4e47-b673-480449a8bf32)

For English, final model performance for a large train split (99.5%) is as follows:

| Algorithm   | Word Error Rate % |
|-------------|-------------------|
| CRF         | 4.25%            |
| NN          | 1.21%            |

It should be noted that the CRF model used here is a slightly less optimal but more cost-effective (fewer parameter) implementation. The full-parameter CRF
models totals about 250 MB in size instead of the ~18MB version included here. 

CRF/NN are the recommended algorithms to use.

## Dependencies
### Running Syllabificator

Syllabificator requires the following libraries to operate:
* Pandas
* Numpy
* Chaine
* Python 3.11 environment for the Neural Net (see end of page for instructions).

CRF only requires Chaine to run, however the Neural Net solution will give better performance and is recommended for documents containing more complex word types.

## Usage
### Syllabifying words

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
To call different algorithms, the following commands can be used for the `hyphenate_text` and `hyphenate_word` functions:
| Algorithm   | Command          |
|-------------|---------------|
| Brandt      | `alg='b'`    |
| Liang       | `alg='l'`   |
| Weijters    | `alg='w'`  |
| CRF         | `alg='c'`  |
| Neural Net  | `alg='n'`  |

* **!Note!**  Syllabificator employs custom seperator patterns for the Liang algorithm. Pyphen is the current decoder used but it does not support external libraries. 
As a work-around, the file `dutch_cus_twee.dic` can be placed in the pyphen library index. If it is not present Pyphen will still work but default to the 
native Dutch pattern libraries instead.

### Algorithm specific parameters

Two algorithms have specific parameters that influence their syllabification. For `alg='l'` (which selects liang's algorithm), `pattern=x` 
where `x` is a value between 1 and 4 selects one of four default libraries. Currently, library 4 is the default.

For `alg='w'`, the number of comparisons with other words from the dictionary can be specified through `w_size=x`. If left empty, it will automatically 
select 2000 words to compare against. Note that a higher value means longer computation. The reference dictionary has about 290000 words listed. 
Setting the value to `w_size=290000` is optimal but may take several minutes to compute.

```python
>>> word = 'chocomel'
>>> hyphenate_word(word, alg='w', w_size=200)
'cho-co-me-l'
>>> hyphenate_word(word, alg='w', w_size=20000)
'cho-co-mel'
```

It should be noted that Weijters algorithm picks any random words to compare against, meaning repeated comparisons with smaller `w_size` are likely to produce
different results.

## Performing analyses

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

### Misc

Syllabificator is newly employed and not yet test-proof

### Virtual Environment Instructions for Neural Net

The deep learning model was created using a custom CRF addon only compatible with an older version of Tensorflow. To run it, the requirements.txt
file can be used to recreate the original environment (note that it requires a Python==3.11 environment).

Alternatively, the recreate the environment in full from scratch, the following steps can be performed manually:

* Create a new environment with `python=3.11`
* Install `numpy==1.24.3` and `pandas==2.2.2`
* Install `tensorflow==2.13.0`
* Install `tensorflow-addons==0.22.0`
* Install `keras_crf==0.3.0`
* Install `chaine==3.12.1`




