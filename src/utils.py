import json

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