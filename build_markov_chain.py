import json
import os
import string
import time

from markov_chain import MarkovChain

def add_file_to_markov(markov_chain, filename):
    lines = []
    words = []
    with open(filename) as input_file:
        lines = input_file.readlines()
        
    for line in lines:
        for word in line.split():
            current_word = word.translate(str.maketrans('', '', string.punctuation))
            current_word = current_word.replace("\"", "")
            current_word = current_word.lower()
            if current_word:
                words.append(current_word)
    for i in range(len(words)):
        try:
            first = words[i]
            second = words[i + 1]
            markov_chain.add(first, second)
        except IndexError:
            pass

def test_markov_chain(markov_filename, word_count):
    markov_chain = None
    with open(markov_filename) as file:
        text = file.read()
        json_parsed = json.loads(text)
        markov_chain = MarkovChain(**json_parsed)
    if markov_chain is not None:
        for i in range(20):
            word = "what"
            generated_text = word + " "
            for i in range(word_count):
                next_word = markov_chain.random_step(word)
                if next_word:
                    generated_text += next_word + " "
                    word = next_word
                else:
                    break

            generated_text = generated_text.rstrip() + "?"
            with open(os.path.join("out", str(time.time()) + ".txt"), "w") as output:
                output.write(generated_text)
        
        frequencies = markov_chain.get_accumulated_frequencies("what")
        with open("frequencies.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(frequencies))
        with open("test.txt", "w", encoding="utf-8") as file:
            file.write(json.dumps(sorted(frequencies.values())))

def create_reddit_markov_chain(markov_chain_filename):
    markov_chain = MarkovChain()

    directory = os.path.join("data", "askreddit_posts")
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            print("adding", filename)
            add_file_to_markov(markov_chain, os.path.join(directory, filename))
    
    dump = json.dumps(markov_chain.__dict__)
    with open(markov_chain_filename, "w") as file:
        file.write(dump)

def create_simple_markov_chain(text_filename, markov_chain_filename):
    markov_chain = MarkovChain()

    add_file_to_markov(markov_chain, "drseuss.txt")
    dump = json.dumps(markov_chain.__dict__)
    with open(markov_chain_filename, "w", encoding="utf-8") as file:
       file.write(dump)

    print(markov_chain.step("the", 0.14))

def create_super_test_chain(markov_chain_filename):
    markov_chain = MarkovChain()

    markov_chain.add("the", "cat")
    markov_chain.add("the", "hat")
    markov_chain.add("the", "bat")
    markov_chain.add("the", "gnat")

    with open(markov_chain_filename, "w", encoding="utf-8") as file:
        file.write(json.dumps(markov_chain.__dict__))

if __name__ == "__main__":
    create_simple_markov_chain("drseuss.txt", "markov_chain.json")