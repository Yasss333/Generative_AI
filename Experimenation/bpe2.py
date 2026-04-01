vocab = {
    "i": 1,
    "love": 2,
    "cod": 3,
    "ing": 4,
    "play": 5,
    "<UNK>": 0
}



def subword_tokenize(word):
    tokens = []
    
    i = 0
    while i < len(word):
        # try 3-letter chunk
        chunk = word[i:i+3]
        
        if chunk in vocab:
            tokens.append(vocab[chunk])
            i += 3
        else:
            tokens.append(vocab["<UNK>"])
            i += 1
            
    return tokens



print(subword_tokenize("coding"))