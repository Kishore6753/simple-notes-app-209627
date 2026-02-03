"""Pydantic schemas for note resources."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class NoteBase(BaseModel):
    """Shared fields for creating/updating notes."""

    title: str = Field(..., min_length=1, max_length=200, description="Short note title.")
    content: str = Field(..., min_length=1, max_length=20000, description="Full note content.")

    @field_validator("title")
    @classmethod
    def _title_not_blank(cls, v: str) -> str:
        v2 = v.strip()
        if not v2:
            raise ValueError("title must not be blank")
        return v2

    @field_validator("content")
    @classmethod
    def _content_not_blank(cls, v: str) -> str:
        v2 = v.strip()
        if not v2:
            raise ValueError("content must not be blank")
        return v2


class NoteCreate(NoteBase):
    """Request body for creating a note."""


class NoteUpdate(BaseModel):
    """Request body for updating a note (partial update not supported; both fields required)."""

    title: str = Field(..., min_length=1, max_length=200, description="Short note title.")
    content: str = Field(..., min_length=1, max_length=20000, description="Full note content.")

    @field_validator("title")
    @classmethod
    def _title_not_blank(cls, v: str) -> str:
        v2 = v.strip()
        if not v2:
            raise ValueError("title must not be blank")
        return v2

    @field_validator("content")
    @classmethod
    def _content_not_blank(cls, v: str) -> str:
        v2 = v.strip()
        if not v2:
            raise ValueError("content must not be blank")
        return v2


class Note(NoteBase):
    """API representation of a note."""

    id: int = Field(..., description="Note unique identifier.")
    created_at: datetime = Field(..., description="Creation timestamp (ISO8601).")
    updated_at: datetime = Field(..., description="Last update timestamp (ISO8601).")


class NoteListResponse(BaseModel):
    """Response body for listing notes."""

    items: list[Note] = Field(..., description="Notes ordered by updated_at desc.")
    total: int = Field(..., ge=0, description="Total number of notes returned.")
