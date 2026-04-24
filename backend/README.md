# Mimic Hunter Backend

Run:

```bash
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

Endpoints:
- `GET /health`
- `POST /compare-files`

## Run Terminal Version (Windows CMD, Local)

From the project root :

```bat
pip install -r backend\requirements.txt
python backend\app\terminal_based_code.py
```

When prompted with `Enter folder path:`, provide a folder that contains `.txt` files.

Valid examples:

```text
C:\path\to\your\documents_folder
"C:\path\to\your\documents_folder"
```

Important:
- Input must be a **folder path**, not a file path.
- **Do not input `.zip` files** in terminal mode.
- The folder should contain at least two `.txt` files.
