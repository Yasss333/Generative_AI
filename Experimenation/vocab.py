vocab={
    "hello":1,
    "Yash":2,
    "do":3,
    "ok":4
}


def tokenizer(sentence):
    words=sentence.split()
    result=[]
    for word in words:
        if(vocab.get(word)):
            result.append(f"({word},{vocab[word]})")
        else:
            result.append(f"Not in vocab {word}")
    return result
    # return [vocab[word] for word in words ]


print(tokenizer("Yash do ok"))