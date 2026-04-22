# Mimic Hunter Backend

Run:

```bash
pip install -r backend/requirements.txt
uvicorn app.main:app --reload --app-dir backend
```

Endpoints:
- `GET /health`
- `POST /compare-files`
