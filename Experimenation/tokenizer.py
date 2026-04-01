vocab={
    "I":1,
    "am":2,
    "ok":3,
    "<UNK>":0
}

def tokenizer(sentence):
    words=sentence.lower().split()
    # print("Words",words)
    tokens=[]
    for word in words:
        if word in vocab:
            tokens.append(vocab[word])
        else:
            tokens.append(vocab["<UNK>"])

    return tokens         
# tokenizer("HEy i ma na yash ")

print(tokenizer("I     am ok     \n"))
print(tokenizer("okokookok"))