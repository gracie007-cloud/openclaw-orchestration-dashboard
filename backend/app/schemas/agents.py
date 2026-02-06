from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import field_validator
from sqlmodel import SQLModel

from app.schemas.common import NonEmptyStr


def _normalize_identity_profile(
    profile: object,
) -> dict[str, str] | None:
    if not isinstance(profile, Mapping):
        return None
    normalized: dict[str, str] = {}
    for raw_key, raw in profile.items():
        if raw is None:
            continue
        key = str(raw_key).strip()
        if not key:
            continue
        if isinstance(raw, list):
            parts = [str(item).strip() for item in raw if str(item).strip()]
            if not parts:
                continue
            normalized[key] = ", ".join(parts)
            continue
        value = str(raw).strip()
        if value:
            normalized[key] = value
    return normalized or None


class AgentBase(SQLModel):
    board_id: UUID | None = None
    name: NonEmptyStr
    status: str = "provisioning"
    heartbeat_config: dict[str, Any] | None = None
    identity_profile: dict[str, Any] | None = None
    identity_template: str | None = None
    soul_template: str | None = None

    @field_validator("identity_template", "soul_template", mode="before")
    @classmethod
    def normalize_templates(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value

    @field_validator("identity_profile", mode="before")
    @classmethod
    def normalize_identity_profile(cls, value: Any) -> Any:
        return _normalize_identity_profile(value)


class AgentCreate(AgentBase):
    pass


class AgentUpdate(SQLModel):
    board_id: UUID | None = None
    is_gateway_main: bool | None = None
    name: NonEmptyStr | None = None
    status: str | None = None
    heartbeat_config: dict[str, Any] | None = None
    identity_profile: dict[str, Any] | None = None
    identity_template: str | None = None
    soul_template: str | None = None

    @field_validator("identity_template", "soul_template", mode="before")
    @classmethod
    def normalize_templates(cls, value: Any) -> Any:
        if value is None:
            return None
        if isinstance(value, str):
            value = value.strip()
            return value or None
        return value

    @field_validator("identity_profile", mode="before")
    @classmethod
    def normalize_identity_profile(cls, value: Any) -> Any:
        return _normalize_identity_profile(value)


class AgentRead(AgentBase):
    id: UUID
    is_board_lead: bool = False
    is_gateway_main: bool = False
    openclaw_session_id: str | None = None
    last_seen_at: datetime | None
    created_at: datetime
    updated_at: datetime


class AgentHeartbeat(SQLModel):
    status: str | None = None


class AgentHeartbeatCreate(AgentHeartbeat):
    name: NonEmptyStr
    board_id: UUID | None = None


class AgentNudge(SQLModel):
    message: NonEmptyStr
