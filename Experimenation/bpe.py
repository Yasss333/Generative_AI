words = ["low", "lower", "newest"]


word_splits = [list(word) for word in words]
# print(word_splits)
from collections import Counter

def get_pairs(word_splits):
    pairs = Counter()
    
    for word in word_splits:
        for i in range(len(word)-1):
            pair = (word[i], word[i+1])
            pairs[pair] += 1
            
    return pairs

# print(get_pairs(word_splits))
pairs = get_pairs(word_splits)
best_pair = max(pairs, key=pairs.get)
# print(best_pair)

def merge_pair(pair, word_splits):
    new_splits = []
    
    for word in word_splits:
        new_word = []
        i = 0
        
        while i < len(word):
            if i < len(word)-1 and (word[i], word[i+1]) == pair:
                new_word.append(word[i] + word[i+1])
                i += 2
            else:
                new_word.append(word[i])
                i += 1
                
        new_splits.append(new_word)
        
    return new_splits


for _ in range(5):
    pairs = get_pairs(word_splits)
    best_pair = max(pairs, key=pairs.get)
    word_splits = merge_pair(best_pair, word_splits)
    print(word_splits)