import argparse
import json
import pathlib
import random
import time

import numpy as np
import praw
import tensorflow as tf
import tensorflow.keras as keras

from utils import load_markov_chain

def connect_to_reddit(credentials):
    reddit = praw.Reddit(client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        password=credentials["password"],
        user_agent=credentials["user_agent"],
        username=credentials["username"]
    )
    
    reddit.validate_on_submit = True
    return reddit

def submit_to_profile(reddit, username, title, selftext=""):
    subreddit = reddit.subreddit("u_" + username)
    subreddit.submit(title, selftext=selftext)

def generate_text(markov_chain, model, iterations):
    start_id = random.randrange(0, markov_chain.last_token_id)
    text = []
    for i in range(iterations):
        vector = tf.one_hot(start_id, markov_chain.last_token_id)
        in_vector = np.append(vector, random.uniform(0, 1))
        
        out = model.predict(np.array([in_vector]))
        out_id = tf.keras.backend.eval(tf.argmax(out[0]))
        out_word = markov_chain.tokens_by_id[out_id]
        
        text.append(out_word)
        start_id = out_id
        
    return text

def generate_post(markov_chain, model):
    title = " ".join(generate_text(markov_chain, model, random.randrange(4, 10)))
    lines = []
    for i in range(3):
        line = generate_text(markov_chain, model, random.randrange(100, 200))
        lines.append(" ".join(line))
        
    selftext = "\n\n".join(lines)
    
    return (title, selftext)

def generate_and_post(reddit, username, markov_chain, model):
        title, selftext = generate_post(markov_chain, model)
        submit_to_profile(reddit, username, title, selftext=selftext)

def schedule_posting_and_lock(reddit, username, markov_chain, model, interval=300):
    start_time = time.time()
    while True:
        generate_and_post(reddit, username, markov_chain, model)
        time.sleep(interval - ((time.time() - start_time) % interval))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Submit a neural network post to a Reddit bot profile using the supplied credentials")
    parser.add_argument("-c", "--configfile", help="Reddit configuration file in JSON format", type=argparse.FileType("r"), default=pathlib.Path(__file__).parents[1] / "credentials.json")
    arguments = parser.parse_args()
    
    credentials = json.load(arguments.configfile)
    reddit = connect_to_reddit(credentials)
    
    markov_chain = load_markov_chain(pathlib.Path(__file__).parents[1] / "markov_chain.json")
    model = keras.models.load_model(pathlib.Path(__file__).parents[1], compile=True)

    schedule_posting_and_lock(reddit, credentials["username"], markov_chain, model, interval=60)
    