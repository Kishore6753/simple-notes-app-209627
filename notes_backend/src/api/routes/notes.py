"""Notes CRUD API routes."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, Path, status

from src.api.repositories.notes_repo import (
    create_note as repo_create_note,
    delete_note as repo_delete_note,
    get_note as repo_get_note,
    list_notes as repo_list_notes,
    update_note as repo_update_note,
)
from src.api.schemas.notes import Note, NoteCreate, NoteListResponse, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get(
    "",
    response_model=NoteListResponse,
    summary="List notes",
    description="Returns all notes ordered by updated_at descending.",
    operation_id="list_notes",
)
def list_notes():
    """List notes ordered by updated_at DESC."""
    items = repo_list_notes()
    return {"items": items, "total": len(items)}


@router.get(
    "/{id}",
    response_model=Note,
    summary="Get note",
    description="Fetch a single note by its id.",
    operation_id="get_note",
)
def get_note(
    id: int = Path(..., ge=1, description="Note id (positive integer)."),
):
    """Fetch a note by id."""
    note = repo_get_note(id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


@router.post(
    "",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    summary="Create note",
    description="Create a new note. Server sets created_at and updated_at timestamps (ISO8601).",
    operation_id="create_note",
)
def create_note(payload: NoteCreate):
    """Create a new note."""
    try:
        return repo_create_note(title=payload.title, content=payload.content)
    except Exception as exc:
        # Avoid leaking internal DB details; still provide helpful message.
        raise HTTPException(status_code=500, detail="Failed to create note") from exc


@router.put(
    "/{id}",
    response_model=Note,
    summary="Update note",
    description="Update an existing note. Server updates updated_at timestamp (ISO8601).",
    operation_id="update_note",
)
def update_note(
    payload: NoteUpdate,
    id: int = Path(..., ge=1, description="Note id (positive integer)."),
):
    """Update an existing note."""
    try:
        updated = repo_update_note(note_id=id, title=payload.title, content=payload.content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to update note") from exc

    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return updated


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete note",
    description="Delete a note by id.",
    operation_id="delete_note",
)
def delete_note(
    id: int = Path(..., ge=1, description="Note id (positive integer)."),
):
    """Delete a note by id."""
    try:
        deleted = repo_delete_note(id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Failed to delete note") from exc

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return None
