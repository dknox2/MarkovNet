import random

class MarkovChain:
    
    def __init__(self):
        self.chain = {}
        self.counts = {}
        
    def add(self, first, second):
        if first not in self.chain:
            self.chain[first] = {}
        if second not in self.chain[first]:
            self.chain[first][second] = 0.0
        if first not in self.counts:
            self.counts[first] = {}
        if second not in self.counts[first]:
            self.counts[first][second] = 0
        
        self.counts[first][second] += 1
        self.normalize_probabilities(first)
    
    def random_step(self, first):
        n = random.uniform(0, 1)
        return self.step(first, n)

    def step(self, first, n):
        accumulator = 0.0
        for second, probability in self.chain[first].items():
            accumulator += probability
            if accumulator >= n:
                return second

        return None

    def normalize_probabilities(self, first):
        total_following_words = self.count_following(first)
        for second in self.chain[first]:
            count = self.counts[first][second]
            probability = count / total_following_words
            self.chain[first][second] = probability
        
    def count_following(self, first):
        return sum(self.counts[first].values())