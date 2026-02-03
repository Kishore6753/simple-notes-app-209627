"""SQLite repository for notes CRUD."""

from __future__ import annotations

import sqlite3
from datetime import datetime, timezone
from typing import Dict, List, Optional

from src.api.db import get_connection, row_to_dict


def _now_iso() -> str:
    """Return an ISO8601 timestamp in UTC."""
    return datetime.now(timezone.utc).isoformat()


def _parse_note_row(row: sqlite3.Row) -> Dict:
    """Convert a note row into an API-friendly dict (datetime fields as ISO strings)."""
    d = row_to_dict(row)
    # Keep timestamps as strings; Pydantic will parse them into datetimes.
    return d or {}


# PUBLIC_INTERFACE
def list_notes() -> List[Dict]:
    """List notes ordered by updated_at DESC (read-only operation)."""
    conn = get_connection()
    try:
        cur = conn.execute(
            """
            SELECT id, title, content, created_at, updated_at
            FROM notes
            ORDER BY updated_at DESC
            """
        )
        rows = cur.fetchall()
        return [_parse_note_row(r) for r in rows]
    finally:
        conn.close()


# PUBLIC_INTERFACE
def get_note(note_id: int) -> Optional[Dict]:
    """Fetch a single note by id."""
    conn = get_connection()
    try:
        cur = conn.execute(
            """
            SELECT id, title, content, created_at, updated_at
            FROM notes
            WHERE id = ?
            """,
            (note_id,),
        )
        row = cur.fetchone()
        return _parse_note_row(row) if row else None
    finally:
        conn.close()


# PUBLIC_INTERFACE
def create_note(title: str, content: str) -> Dict:
    """Create a note and return the created record."""
    conn = get_connection()
    try:
        now = _now_iso()
        cur = conn.execute(
            """
            INSERT INTO notes (title, content, created_at, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (title, content, now, now),
        )
        conn.commit()
        note_id = int(cur.lastrowid)
        created = get_note(note_id)
        # get_note opens a separate connection; for consistency return that.
        if created is None:
            # Very unlikely; still handle.
            raise RuntimeError("Failed to fetch created note")
        return created
    finally:
        conn.close()


# PUBLIC_INTERFACE
def update_note(note_id: int, title: str, content: str) -> Optional[Dict]:
    """Update an existing note, returning the updated record or None if not found."""
    conn = get_connection()
    try:
        now = _now_iso()
        cur = conn.execute(
            """
            UPDATE notes
            SET title = ?, content = ?, updated_at = ?
            WHERE id = ?
            """,
            (title, content, now, note_id),
        )
        conn.commit()
        if cur.rowcount == 0:
            return None
        updated = get_note(note_id)
        if updated is None:
            raise RuntimeError("Failed to fetch updated note")
        return updated
    finally:
        conn.close()


# PUBLIC_INTERFACE
def delete_note(note_id: int) -> bool:
    """Delete a note by id. Returns True if deleted, False if not found."""
    conn = get_connection()
    try:
        cur = conn.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        conn.commit()
        return cur.rowcount > 0
    finally:
        conn.close()
