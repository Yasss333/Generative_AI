from __future__ import annotations

import tiktoken


def demo_tokenization(text: str, model: str = "gpt-4o") -> None:
    """Encode text into tokens and decode it back for learning."""
    encoder = tiktoken.encoding_for_model(model)
    tokens = encoder.encode(text)
    decoded = encoder.decode(tokens)

    print(f"Model: {model}")
    print(f"Original text: {text}")
    print(f"Tokens: {tokens}")
    print(f"Decoded text: {decoded}")
    print(f"Token count: {len(tokens)}")


if __name__ == "__main__":
    demo_tokenization("Hi, this is Yash.")