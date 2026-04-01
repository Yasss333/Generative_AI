next_word={
    "i love":"code",
    "yeah":"buddy"
}

def nextword(sentence):
    words=[]
    sentence=sentence.lower()
    # for token in next_word:
    if sentence in next_word:
        words.append(next_word[sentence])
    else:
        words.append("Something")
    

    return words

print(nextword("i love"))