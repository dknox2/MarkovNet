import random

class MarkovChain():
    
    def __init__(self, **kwargs):
        if len(kwargs) == 5:
            self.chain = kwargs["chain"]
            self.counts = kwargs["counts"]
            self.token_ids = kwargs["token_ids"]
            self.tokens_by_id = kwargs["tokens_by_id"]
            self.last_token_id = kwargs["last_token_id"]
        else:
            self.chain = {}
            self.counts = {}
            self.token_ids = {}
            self.tokens_by_id = {}
            self.last_token_id = 0

    def add(self, first, second):
        if first not in self.chain:
            self.chain[first] = {}
        if second not in self.chain[first]:
            self.chain[first][second] = 0.0
        if first not in self.counts:
            self.counts[first] = {}
        if second not in self.counts[first]:
            self.counts[first][second] = 0

        if first not in self.token_ids:
            self.token_ids[first] = self.last_token_id
            self.tokens_by_id[self.last_token_id] = first
            self.last_token_id += 1
        if second not in self.token_ids:
            self.token_ids[second] = self.last_token_id
            self.tokens_by_id[self.last_token_id] = second
            self.last_token_id += 1
        
        self.counts[first][second] += 1
        self.normalize_probabilities(first)
    
    def random_step(self, first):
        n = random.uniform(0, 1)
        return self.step(first, n)

    def step(self, first, n):
        accumulator = 0.0

        last_visited = None
        for second, probability in self.chain[first].items():
            accumulator += probability
            last_visited = second
            if accumulator >= n:
                return second

        return last_visited

    def normalize_probabilities(self, first):
        total_following_words = sum(self.counts[first].values())
        for second in self.chain[first]:
            count = self.counts[first][second]
            probability = count / total_following_words
            self.chain[first][second] = probability
    
    def get_accumulated_frequencies(self, first):
        frequencies = {}
        accumulator = 0.0

        for second, probability in self.chain[first].items():
            accumulator += probability
            frequencies[second] = accumulator

        return frequencies

    def get_normalized_token_id(self, token):
        return self.token_ids[token] / self.last_token_id