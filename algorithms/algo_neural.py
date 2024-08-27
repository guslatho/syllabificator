import os
import numpy as np
import pandas as pd
import tensorflow as tf

from tensorflow.keras.callbacks import Callback
from keras.callbacks import Callback, ModelCheckpoint

from tensorflow import keras
from keras_crf import CRFModel

# To disable warning message during model compilation 
import logging
tf.get_logger().setLevel('ERROR')

# Constants used while training, do not change
ALPHABET = 'abcdefghijklmnopqrstuvwxyz@#$%'
MAX_WL = 34  
INPUT_SHAPE = (34, 5)
ALPHABET_SIZE = 31
LAYER_UNITS = 128
DROPOUT_VALUE = 0.3
TAGS = 3

# Misc functions used while converting data to interpretable by model
def alphab(character):
    return ALPHABET.index(character)+1
def solution_to_list(string):
    return [int(i) for i in string]
def pad(coding):
    coding_length = len(coding)
    return [0]*(MAX_WL-coding_length) + coding

# Novel net inputs words split into 5-char window, function below to pre-process accordingly
def words_to_window_array(dehyphenated_words):
    output_list = []
    # Process each word
    for index in range(len(dehyphenated_words)):
        word = dehyphenated_words.iloc[index]
        pad_size = 34 - len(word)
        word = '@#' + word + '$%'
        output = []
        for char in range(2, len(word)-2):
            m2 = alphab(word[char-2])
            m1 = alphab(word[char-1])
            n = alphab(word[char])
            p1 = alphab(word[char+1])
            p2 = alphab(word[char+2])
            output.append([m2, m1, n, p1, p2])
        for i in range(pad_size):
            output.insert(0, [0, 0, 0, 0, 0])
        output_list.append(output)
        if str(index)[-5:] == '00000' or str(index)[-5:] == '50000':
            print(f'...Processed {index} words...')
    return np.array(output_list)

# Load a CRFModel. 
def crf_model_loader(model_path, base, tags):
    # Define a function that creates CRFModel instance
    def custom_model(*args, **kwargs):
        if 'name' in kwargs:
            kwargs.pop('name')  # Remove 'name' argument if present
        # Create CRFModel instance using base model and tags
        return CRFModel(model=base, units=tags, *args, **kwargs)
    # Load the model using custom_objects with the defined function
    loaded_model = tf.keras.models.load_model(model_path, custom_objects={"CRFModel": custom_model})
    return loaded_model

# Model has to be compiled first before it can be loaded (workaround, CRFModel does not load otherwise)
inputs = tf.keras.Input(shape=INPUT_SHAPE)
E = keras.layers.TimeDistributed(keras.layers.Embedding(input_dim=ALPHABET_SIZE, output_dim=LAYER_UNITS))(inputs)  
E = keras.layers.TimeDistributed(keras.layers.Dropout(DROPOUT_VALUE))(E)
C = keras.layers.TimeDistributed(keras.layers.Conv1D(filters=40, kernel_size=3, strides=1, padding='same'))(E)
C = keras.layers.TimeDistributed(keras.layers.MaxPooling1D(pool_size=3, strides=1, padding='same'))(C)
C = keras.layers.TimeDistributed(keras.layers.Flatten())(C)
LSTM = keras.layers.Bidirectional(tf.keras.layers.LSTM(LAYER_UNITS, return_sequences=True))(C)
LSTM = keras.layers.Bidirectional(tf.keras.layers.LSTM(LAYER_UNITS, return_sequences=True))(LSTM)
base = tf.keras.Model(inputs=inputs, outputs=LSTM)
model = CRFModel(base, TAGS)
model.compile(
    optimizer=tf.keras.optimizers.Adam(3e-4),
    metrics=['acc'],
    )

# Establish model path, load
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'neural_model.h5')
nnmodel = crf_model_loader(model_path, base, TAGS)

# Syllabificate a word
def nn_syllabificate(input_word):

    # Process, predict
    word = pd.Series([input_word])
    word = words_to_window_array(word)
    prediction = nnmodel.predict(word, verbose=0)[0][0]
    hyphens = [i for i in prediction.tolist() if i!= 0]

    word_output = []

    for letter in range(len(input_word)):
        if hyphens[letter] == 2:
            word_output.append(input_word[letter]+'-')
        else:
            word_output.append(input_word[letter])

    return ''.join(word_output)
