# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:33:04 2020

@author: Dylan
"""

import json
import random

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras as keras
import matplotlib.pyplot as pyplot
from tensorflow.keras.models import Sequential, save_model, load_model

from markov_chain import MarkovChain

def load_markov_chain(filename):
    markov_chain = None
    with open(filename) as file:
        text = file.read()
        parsed = json.loads(text)
        markov_chain = MarkovChain(**parsed)
        markov_chain.tokens_by_id = {int(k):str(v) for k,v in markov_chain.tokens_by_id.items()}
        markov_chain.token_ids = {str(k):int(v) for k,v in markov_chain.token_ids.items()}
    
    return markov_chain

def build_dset(markov_chain, one_hot_vectors):
    inputs = []
    labels = []

    for word in markov_chain.chain.keys():
        following_words = len(markov_chain.chain[word])
        increment = 1.0 / (following_words * 3)
        accumulator = 0.0
        
        while accumulator < 1.0:
            second = markov_chain.step(word, accumulator)
            input_id = markov_chain.token_ids[word]
            in_vector = np.copy(one_hot_vectors[input_id])
            in_vector = np.append(in_vector, accumulator)
            inputs.append(in_vector)
            
            target_id = markov_chain.token_ids[second]
            labels.append(target_id)
            
            accumulator += increment
    
    return (np.array([inputs]), np.array([labels]))
    
def write_dset_to_file(inputs, labels):
    with open("inputs.json", "w") as inputs_file:
        inputs_file.write(json.dumps(inputs.tolist()))
    with open("labels.json", "w") as labels_file:
        labels_file.write(json.dumps(labels.tolist()))

def load_dset(inputs_filename, labels_filename):
    inputs = []
    labels = []
    
    with open(inputs_filename) as inputs_file:
        inputs_text = inputs_file.read()
        inputs = json.loads(inputs_text)
    
    with open(labels_filename) as labels_file:
        labels_text = labels_file.read()
        labels = json.loads(labels_text)
    
    return (np.array(inputs), np.array(labels))

def build_model(class_size):
    model = keras.Sequential([
            keras.layers.Input((class_size + 1,)),
            
            keras.layers.Dense(50),
            keras.layers.Activation("elu"),
            keras.layers.BatchNormalization(),
            
            keras.layers.Dense(50),
            keras.layers.Activation("elu"),
            keras.layers.BatchNormalization(),
            
            keras.layers.Dense(50),
            keras.layers.Activation("elu"),
            keras.layers.BatchNormalization(),
            
            keras.layers.Dense(class_size), 
            keras.layers.Activation('softmax'),
        ])
    
    model.compile(
                optimizer=keras.optimizers.SGD(learning_rate=0.001,
                                               momentum=0.9),
                metrics=['accuracy'],
                loss="sparse_categorical_crossentropy"
                )
    
    return model

def build_dset_and_train(markov_chain, vectors):
    inputs, labels = build_dset(markov_chain, vectors)
    model = build_model(markov_chain.last_token_id)
    history = model.fit(x=inputs[0], y=labels[0], epochs=100, validation_split=0.3)
    model.save(".")
    
    pyplot.plot(history.history["loss"], label="loss")
    pyplot.plot(history.history["val_loss"], label="val_loss")
    pyplot.plot(history.history["accuracy"], label="accuracy")
    pyplot.plot(history.history["val_accuracy"], label="val_accuracy")
    pyplot.legend()
    
    return model

if __name__ == "__main__":
    markov_chain = load_markov_chain("markov_chain.json")
    
    vectors = tf.keras.utils.to_categorical(
        list(markov_chain.tokens_by_id.keys()), dtype='float32'
    )
    
    model = load_model(".", compile=True)
   
    test_id = markov_chain.token_ids["the"]
    in_vector = np.copy(vectors[test_id])
    in_vector = np.append(in_vector, 0.14)
    
    print(in_vector.shape)
    print(in_vector)
    out = model.predict(np.array([in_vector]))
    print(out[0])
    print(np.round(out[0]))
    
    out_id = np.argmax(out[0], axis=0)
    print(markov_chain.tokens_by_id[out_id.item()])