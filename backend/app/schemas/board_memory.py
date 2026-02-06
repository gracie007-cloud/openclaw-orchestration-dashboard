from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel

from app.schemas.common import NonEmptyStr


class BoardMemoryCreate(SQLModel):
    content: NonEmptyStr
    tags: list[str] | None = None
    source: str | None = None


class BoardMemoryRead(BoardMemoryCreate):
    id: UUID
    board_id: UUID
    created_at: datetime
