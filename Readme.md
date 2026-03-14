# Generative AI - Learning Repository

This repository contains my lecture-wise learning experiments for Generative AI.

## Lecture 01

### Files
- `lect-01/tokenization.py`: shows how text is converted to tokens using `tiktoken`.
- `lect-01/embeddings.py`: loads `OPENAI_API_KEY` from `.env` and fetches embeddings from OpenAI.
- `lect-01/requirements.txt`: Python dependencies needed for lecture 01.
- `lect-01/.env.example`: template for environment variables.

### Setup
1. Create and activate virtual environment (PowerShell):
   ```powershell
   cd lect-01
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Create your local `.env` file:
   ```powershell
   Copy-Item .env.example .env
   ```
   Then put your real OpenAI API key inside `.env`.

### Run
```powershell
python tokenization.py
python embeddings.py
```