# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:33:04 2020

@author: Dylan
"""

import json
import pathlib
import pickle
import random

import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
import matplotlib.pyplot as pyplot

from markov_chain import MarkovChain
from utils import load_markov_chain

def build_dset(markov_chain):
    inputs = []
    labels = []
    
    filepath = pathlib.Path(__file__).parents[1] / "data" / "train"
    for word in markov_chain.chain.keys():
        print(word)
        following_words = len(markov_chain.chain[word])
        increment = 1.0 / (following_words * 2)
        accumulator = 0.0
        
        while accumulator < 1.0:
            second = markov_chain.step(word, accumulator)
            input_id = markov_chain.token_ids[word]
            vector = tf.one_hot(input_id, markov_chain.last_token_id)
            vector = np.append(vector, accumulator)
            inputs.append(vector)
            
            target_id = markov_chain.token_ids[second]
            labels.append(target_id)
            
            accumulator += increment
    
    with open(filepath / "in.pkl", "wb") as file:
        pickle.dump(inputs, file)

    with open(filepath / "labels.pkl", "wb") as file:
        pickle.dump(labels, file)
    
def load_dset_index(index):
    inputs = []
    labels = []
    
    inputs_filename = pathlib.Path(__file__).parents[1] / "data" / "train" / (str(index) + "_in.pkl")
    labels_filename = pathlib.Path(__file__).parents[1] / "data" / "train" / (str(index) + "_labels.pkl")
    
    with open(inputs_filename, "rb") as file:
        inputs = pickle.load(file)
    with open(labels_filename, "rb") as file:
        labels = pickle.load(file)
    
    return (np.array(inputs), np.array(labels))

def load_dset():
    inputs = []
    labels = []
    
    inputs_filename = pathlib.Path(__file__) / "data" / "train" / "in.pkl"
    labels_filename = pathlib.Path(__file__) / "data" / "train" / "labels.pkl"
    
    with open(inputs_filename, "rb") as file:
        inputs = pickle.load(file)
    with open(labels_filename, "rb") as file:
        labels = pickle.load(file)
    
    return (np.array(inputs), np.array(labels))

def build_model(class_size):
    model = keras.Sequential([
            keras.layers.Input((class_size + 1,)),
            
            keras.layers.Dense(300),
            keras.layers.Activation("relu"),
            keras.layers.BatchNormalization(),
            #keras.layers.Dropout(0.2),
            
            keras.layers.Dense(200),
            keras.layers.Activation("relu"),
            keras.layers.BatchNormalization(),
            #keras.layers.Dropout(0.2),
            
            keras.layers.Dense(200),
            keras.layers.Activation("relu"),
            keras.layers.BatchNormalization(),
            #keras.layers.Dropout(0.2),
            
            keras.layers.Dense(class_size), 
            keras.layers.Activation('softmax'),
        ])
    
    model.compile(
                optimizer=keras.optimizers.SGD(learning_rate=0.01,
                                               momentum=0.9),
                metrics=['accuracy'],
                loss="sparse_categorical_crossentropy"
                )
    
    return model

def build_and_train_model(class_size, iterations):
    print("building model")
    model = build_model(class_size)
    
    for i in range(iterations):
        print(i)
        inputs, labels = load_dset_index(i)
        history = None
        try:
            history = model.fit(x=inputs, y=labels, epochs=100, validation=0.3)
        except ValueError:
            history = model.fit(x=inputs, y=labels, epochs=100)

    model.save(pathlib.Path(__file__).parents[1])
    
    return model

def build_and_train_model(class_size):
    print("building model")
    model = build_model(class_size)
    
    inputs, labels = load_dset()
    print(len(labels))
    history = None
    try:
        history = model.fit(x=inputs, y=labels, epochs=100)
    except ValueError:
        history = model.fit(x=inputs, y=labels, epochs=100)
 
    model.save(".")
    
    return model

if __name__ == "__main__":
    markov_chain = load_markov_chain("markov_chain.json")
    #build_dset(markov_chain)
    model = build_and_train_model(markov_chain.last_token_id)