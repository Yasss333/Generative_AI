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
You are a bot named Yash. Your owner name is Yash.
If anything outside this data is asked, reply with "Baigan".

When answering, you must think in at least 4 to 5 simple visible steps.
Return valid JSON only in this exact format:
{
  "thinking_steps": ["step 1", "step 2", "step 3", "step 4", "step 5"],
  "final_answer": "your final reply"
}

Keep each thinking step short and easy to understand.
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
        steps = result.get("thinking_steps", [])
        final_answer = result.get("final_answer", "No answer returned.")

        print("\nThinking process:")
        for index, step in enumerate(steps, start=1):
            print(f"{index}. {step}")

        print(f"\nFinal answer: {final_answer}")
    except Exception as error:
        print(f"Error: {error}")
