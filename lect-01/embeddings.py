from __future__ import annotations

import os

from dotenv import load_dotenv
from openai import OpenAI


def get_embedding(text: str, model: str = "text-embedding-3-small") -> list[float]:
    """Return an embedding vector for the provided text."""
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is missing. Add it to your .env file or environment variables."
        )

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(model=model, input=text)
    return response.data[0].embedding


if __name__ == "__main__":
    sample_text = "Learning generative AI one step at a time."
    embedding = get_embedding(sample_text)

    print(f"Input: {sample_text}")
    print(f"Embedding length: {len(embedding)}")
    print(f"First 5 values: {embedding[:5]}")