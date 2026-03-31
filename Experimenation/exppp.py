from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI

# 1. Load documents
docs = ["MongoDB is NoSQL", "React is frontend"]

# 2. Convert to embeddings
embeddings = OpenAIEmbeddings()
print("EMbeidngs : ",embeddings)
# 3. Store in vector DB
db = FAISS.from_texts(docs, embeddings)

# 4. Query
query = "What is MongoDB?"

results = db.similarity_search(query)
print("Results : ",results)
# 5. Send to LLM
llm = OpenAI()
answer = llm(results[0].page_content)

print(answer)