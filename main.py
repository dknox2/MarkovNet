import json
import os
import string
import time

from markov_chain import MarkovChain

def markov_test(filename, word_count):
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
    
    markov_chain = MarkovChain()
    for i in range(len(words)):
        try:
            first = words[i]
            second = words[i + 1]
            markov_chain.add(first, second)
        except IndexError:
            pass
    
    dump = json.dumps(markov_chain.__dict__)
    with open("json_test.json", "w") as file:
        file.write(dump)

    with open("json_test.json") as file:
        text = file.read()
        loaded = json.loads(text)
        loaded = MarkovChain(**loaded)
        markov_chain = loaded

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
        
if __name__ == "__main__":
    average_length = 0
    with open("askreddit_top.txt") as file:
        lengths = []
        lines = file.readlines()
        for line in lines:
            lengths.append(len(line.split()))
        average_length = sum(lengths) / len(lengths)
        average_length = round(average_length)

    for i in range(10):
        markov_test("askreddit_top.txt", 10)