vocab={
    "hello":1,
    "Yash":2
}


def tokenizer(sentence):
    words=sentence.split()
    return [vocab[word] for word in words]


print(tokenizer("hello Yash"))