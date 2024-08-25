# Syllabificator

Library and tool for syllabifying Dutch/English words and comparing output from different syllabification algorithms.

## General
### Description

Syllabificator is a tool for syllabifying words, meaning to split **words** into **pho-ne-tic** **com-pli-ant** **syl-la-bles**. It works
by directly employing algorithms from external libraries (like Pyphen) supplemented with implementations of algorithms manually coded.
There are currently five different algorithm that the tool supports:

| Algorithm   | Type          | Dutch | English |
|-------------|---------------|-------|---------|
| Brandt      | Linguistic    | V     | x       |
| Liang       | Algorithmic   | V     | x       |
| Weijters    | Lookup-based  | V     | x       |
| CRF         | Conditional Random Field (Linear Chain)  | V     | V       |
| NN          | Neural Net    | V     | V       |

Note that Syllabificator divides words according to **phonetic pronounciation**, which differs from word dividing based on **spelling conventions**.
See [this page](https://new.reddit.com/r/asklinguistics/comments/1elahiq/what_is_the_point_of_hyphenations_in_dictionaries/) for a brief discussion on the differences.

### Algorithm Performance

Performance of the algorithms was analyzed on different datasets. Below displayed are the word error rate for each set for each algorithm:

![performance_comparison](https://github.com/user-attachments/assets/904c47ff-ebf8-4e47-b673-480449a8bf32)

It should be noted that the CRF metrics displayed above are for a less optimal but more cost-effective (fewer parameter) approach. The full CRF
model performs slightly better but totals about 250 MB in size instead of the ~18MB model included here. CRF/NN are the recommended algorithms
to use as they performed better overall in comparison with the other algorithms.

## Usage
### Running Syllabificator

Syllabificator requires the following libraries to operate:
* Pandas
* Numpy
* Pyphen
* Chaine
  
### Syllabifying words

The most general function syllabifies a string of text into an output with individual syllables. It can be run from the main module,
`main.py`:

```python
>>> text = 'De nieuwsgierige man doorzocht de bibliotheek.'
>>> syllabificate_text(text)
'De nieuws-gie-ri-ge man door-zocht de bi-bli-o-theek.'
```

The `syllabificate_text` function supports non-alpha characters, however does not currently take into consideration special characters
when syllabifying (e.g., `é`)

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
>>> sample_set = pd.read_csv('set_loan_hyphenated_sample.csv', header=None)  # .csv containing hyphenated words seperate by break
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
'Processing...'
'           TP  FP  TN  FN  owe  swe    %ower   %swer   %oler   %sler'
'CORRECT    18   0  56   0    0    0    0.000   0.000   0.000   0.000'
'NO_HYPHEN   0   0  56  18    9    0  100.000   0.000  24.324   0.000'
'Brandt     16   2  54   2    2    2   22.222  22.222   5.405   2.703'
'Liang      18   0  56   0    0    0    0.000   0.000   0.000   0.000'
'CRF        18   0  56   0    0    0    0.000   0.000   0.000   0.000'
'Weijters   12  13  43   6    8    7   88.889  77.778  25.676  17.568'
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
