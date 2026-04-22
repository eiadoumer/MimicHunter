import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router as plagiarism_router
from app.logging_system.logging_utils import configure_logging

logger = configure_logging()

app = FastAPI(title="MimicHunter API", version="1.0.0")

_default_origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://mimic-hunter.vercel.app",
]
_allow = list(_default_origins)

_frontend = os.environ.get("FRONTEND_URL", "").strip().rstrip("/")
if _frontend and _frontend not in _allow:
    _allow.append(_frontend)

_extra = os.environ.get("ALLOWED_ORIGINS", "").strip()
if _extra:
    for part in _extra.split(","):
        origin = part.strip().rstrip("/")
        if origin and origin not in _allow:
            _allow.append(origin)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allow,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plagiarism_router)


@app.on_event("startup")
def startup_event():
    logger.info("MimicHunter API started")
