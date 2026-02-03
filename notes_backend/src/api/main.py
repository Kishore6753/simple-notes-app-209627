"""FastAPI application entrypoint for the notes backend.

Provides REST CRUD endpoints for notes stored in a shared SQLite database.
"""

from __future__ import annotations

import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.notes import router as notes_router

openapi_tags = [
    {
        "name": "system",
        "description": "Service health and meta endpoints.",
    },
    {
        "name": "notes",
        "description": "CRUD APIs for notes. Notes are stored in SQLite with ISO8601 timestamps.",
    },
]


def _get_allowed_origins() -> List[str]:
    """Resolve allowed CORS origins.

    - If FRONTEND_ORIGIN is set, allow that origin (comma-separated supported).
    - Otherwise default to permissive '*' to keep template behavior working.
    """
    raw = os.getenv("FRONTEND_ORIGIN", "").strip()
    if not raw:
        return ["*"]
    return [o.strip() for o in raw.split(",") if o.strip()]


app = FastAPI(
    title="Simple Notes API",
    description="Backend API for a simple notes app (FastAPI + SQLite).",
    version="0.1.0",
    openapi_tags=openapi_tags,
)

# CORS for frontend integration (React dev server / deployed origin).
app.add_middleware(
    CORSMiddleware,
    allow_origins=_get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(notes_router)


@app.get(
    "/",
    tags=["system"],
    summary="Health check",
    description="Basic health check endpoint.",
    operation_id="health_check",
)
def health_check():
    """Return a basic health check response."""
    return {"message": "Healthy"}
