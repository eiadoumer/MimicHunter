# Mimic Hunter

Mimic Hunter is a modular full-stack plagiarism similarity detector:
- **Backend:** FastAPI (`backend/app`)
- **Frontend:** Vite + React + TypeScript (`frontend`)


## Run Terminal Version (Windows CMD, Local)

From the project root :

```bat
pip install -r backend\requirements.txt
python backend\app\terminal_based_code.py
```


## How It Works

1. **Read documents**  
   The system loads `.txt` files and assigns document IDs.

2. **Preprocess text**  
   It applies the preserved pipeline:
   - lowercase
   - punctuation removal
   - token split
   - alphabetic filtering
   - optional stopword removal
   - Porter stemming
   - bigram generation (n-grams of size 2)

3. **Hash-based inverted index**  
   Bigrams are inserted into a custom hash structure using:
   - outer bucket by first character (`a` to `z`)
   - inner index via `h1`, `h2`, and double-hashing probe
   This maps each bigram to the list of document IDs containing it.

4. **Jaccard similarity**  
   For each document pair, similarity is computed as:
   - `intersection / union` on unique bigram sets
   - intersection is checked efficiently through the inverted hash index.

5. **Ranking**  
   Scores are stored in a Red-Black Tree and returned in descending order with labels:
   - High similarity: `>= 0.5`
   - Moderate similarity: `>= 0.25`
   - Low similarity: `< 0.25`

## Quick Run (Important Method)

From project root:

```bash
pip install -r backend/requirements.txt
cd frontend && npm install && cd ..
```

Run backend:

```bash
python -m uvicorn app.main:app --reload --app-dir backend
```

Run frontend (new terminal):

```bash
cd frontend
npm run dev
```

Set frontend API URL in `frontend/.env`:

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```
