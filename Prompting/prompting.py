#zero shot prompting


from dotenv import load_dotenv
from openai import OpenAI
import os 


load_dotenv()

client=OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

System_Prompt="""
hey you are a helpul iassitant answer in one line in json fomat only 
"""
result=client.chat.completions.create(
    model="GPT-4o-mini",
    response_format={"type":"json_object"},
    messages=[
        {"role":"system","content":System_Prompt},
        {"role":"user","content":"WHere is mumbai located ?"}
    ]
)


print(result.choices[0].message.content)