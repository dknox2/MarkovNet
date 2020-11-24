# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 16:33:04 2020

@author: Dylan
"""

import json
import os
import pickle
import random

import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
import matplotlib.pyplot as pyplot

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

def build_dset(markov_chain):
    inputs = []
    labels = []
    
    filepath = os.path.join("data", "train")
    for word in markov_chain.chain.keys():
        print(word)
        following_words = len(markov_chain.chain[word])
        increment = 1.0 / (following_words * 1)
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
    
    with open(os.path.join(filepath, "in.pkl"), "wb") as file:
        pickle.dump(inputs, file)

    with open(os.path.join(filepath, "labels.pkl"), "wb") as file:
        pickle.dump(labels, file)
    
def load_dset_index(index):
    inputs = []
    labels = []
    
    inputs_filename = os.path.join("data", "train", str(index) + "_in.pkl")
    labels_filename = os.path.join("data", "train", str(index) + "_labels.pkl")
    
    with open(inputs_filename, "rb") as file:
        inputs = pickle.load(file)
    with open(labels_filename, "rb") as file:
        labels = pickle.load(file)
    
    return (np.array(inputs), np.array(labels))

def load_dset():
    inputs = []
    labels = []
    
    inputs_filename = os.path.join("data", "train", "in.pkl")
    labels_filename = os.path.join("data", "train", "labels.pkl")
    
    with open(inputs_filename, "rb") as file:
        inputs = pickle.load(file)
    with open(labels_filename, "rb") as file:
        labels = pickle.load(file)
    
    return (np.array(inputs), np.array(labels))

def build_model(class_size):
    model = keras.Sequential([
            keras.layers.Input((class_size + 1,)),
            
            keras.layers.Dense(200),
            keras.layers.Activation("elu"),
            keras.layers.BatchNormalization(),
            
            keras.layers.Dense(200),
            keras.layers.Activation("elu"),
            keras.layers.BatchNormalization(),
            
            keras.layers.Dense(200),
            keras.layers.Activation("elu"),
            keras.layers.BatchNormalization(),
            
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
            history = model.fit(x=inputs, y=labels, epochs=100)
        except ValueError:
            history = model.fit(x=inputs, y=labels, epochs=100)

    model.save(".")
    
    return model

def build_and_train_model(class_size):
    print("building model")
    model = build_model(class_size)
    
    inputs, labels = load_dset()
    history = None
    try:
        history = model.fit(x=inputs, y=labels, epochs=100)
    except ValueError:
        history = model.fit(x=inputs, y=labels, epochs=100)
 
    model.save(".")
    
    return model

def test_model(markov_chain, model, iterations):
    start_id = markov_chain.token_ids["the"]
    vector = tf.one_hot(start_id, markov_chain.last_token_id)
    in_vector = np.copy(vector)
    in_vector = np.append(in_vector, random.uniform(0, 1))
    text = markov_chain.tokens_by_id[start_id] + " "
    for i in range(iterations):
        vector = tf.one_hot(start_id, markov_chain.last_token_id)
        in_vector = np.copy(vector)
        rand = random.uniform(0, 1)
        in_vector = np.append(in_vector, rand)
        
        out = model.predict(np.array([in_vector]))
        out_id = tf.keras.backend.eval(tf.argmax(out[0]))
        out_word = markov_chain.tokens_by_id[out_id]
        text += out_word + " "
        
        start_id = out_id
        
    return text
    

if __name__ == "__main__":
    markov_chain = load_markov_chain("markov_chain.json")
    model = tf.keras.models.load_model(".", compile=True)
    
    for i in range(5):
        start_word = markov_chain.tokens_by_id[random.randrange(0, markov_chain.last_token_id)]
        test_text = test_model(markov_chain, model, random.randint(10, 30))
        print(test_text)
        