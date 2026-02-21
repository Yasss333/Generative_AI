import tiktoken

encoder=tiktoken.encoding_for_model('gpt-4o')

text="Hi this is yash"
tokens=encoder.encode(text)
decoded=encoder.decode(tokens)
print("Tokens",tokens)
print("decoded : ",decoded )

# print("Vocab Size ")