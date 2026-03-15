from dotenv import load_dotenv
from openai import OpenAI
import json
import os


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
)

system_prompt = """
hey you are  personan based AI agent you are my opersiona bit i have given my deatils right next , my name is Yash Mandhare , i study in vesit 3rd year student , i like tp read books 
My birth date is 23 august 2004 ,i like readig books , i like gym my pr are 160 kg deadlift bench 80kg squar 100kg 
i am a sarcastic guy every time you get a query keep it sarcastic 
if any thisng outpof context reply "Humko nahi pata "
Return valid JSON only in this exact format:
{
  "final_answer": "your final reply"
}
example:
what book are you reading now days 
output:ShreemanYogi


""".strip()


def ask_model(user_query: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query},
        ],
    )
    return json.loads(response.choices[0].message.content)


while True:
    query = input("\nAsk something (type 'exit' to quit): ").strip()

    if query.lower() == "exit":
        print("Bye!")
        break

    if not query:
        print("Please type a question.")
        continue

    try:
        result = ask_model(query)
        # steps = result.get("thinking_steps", [])
        final_answer = result.get("final_answer", "No answer returned.")

        print("\nThinking process:")
        # for index, step in enumerate(steps, start=1):
        #     print(f"{index}. {step}")

        print(f"\nFinal answer: {final_answer}")
    except Exception as error:
        print(f"Error: {error}")
