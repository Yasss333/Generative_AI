from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()

client =OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)
system_promt="""You are a bot named Yash , your owner name is Yash
if any thing other then this data asked reply "Baigan"
example
input :What is your name ?
Output:Yash ios my name

"""
completion=client.chat.completions.create(
    model="GPT-4o-mini",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system", "content":system_promt},
        {"role":"user","content":"Hey what is your age "}
    ]
)


print(completion.choices[0].message.content)