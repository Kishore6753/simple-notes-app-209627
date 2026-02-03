"""SQLite database utilities for the notes backend.

The database file is owned by the separate `database` container, but this backend
reads/writes to that same SQLite file path.

We support overriding the path with SQLITE_DB (provided by the platform for the
database container) but default to the known workspace path (db_connection.txt).
"""

from __future__ import annotations

import os
import sqlite3
from typing import Any, Dict, Optional

# Confirmed DB file location (from simple-notes-app-209629/database/db_connection.txt).
_DEFAULT_DB_PATH = "/home/kavia/workspace/code-generation/simple-notes-app-209629/database/myapp.db"


# PUBLIC_INTERFACE
def get_db_path() -> str:
    """Return the SQLite DB file path.

    Uses SQLITE_DB env var when present; otherwise falls back to the known path.
    """
    return os.getenv("SQLITE_DB", _DEFAULT_DB_PATH)


# PUBLIC_INTERFACE
def get_connection() -> sqlite3.Connection:
    """Create a SQLite connection configured for dict-like row access."""
    conn = sqlite3.connect(get_db_path(), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def row_to_dict(row: Optional[sqlite3.Row]) -> Optional[Dict[str, Any]]:
    """Convert a sqlite3.Row to a plain dict."""
    if row is None:
        return None
    return {k: row[k] for k in row.keys()}
