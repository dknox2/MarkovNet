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
    
    word = "the"
    generated_text = word + " "
    for i in range(word_count):
        next_word = markov_chain.random_step(word)
        if next_word:
            generated_text += next_word + " "
            word = next_word
        else:
            break
        
    with open(os.path.join("out", str(time.time()) + ".txt"), "w") as output:
        output.write(generated_text)
        
if __name__ == "__main__":
    for i in range(10):
        markov_test("monty_python.txt", 250)