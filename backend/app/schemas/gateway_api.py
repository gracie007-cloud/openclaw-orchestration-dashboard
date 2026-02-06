from __future__ import annotations

from sqlmodel import SQLModel

from app.schemas.common import NonEmptyStr


class GatewaySessionMessageRequest(SQLModel):
    content: NonEmptyStr


class GatewayResolveQuery(SQLModel):
    board_id: str | None = None
    gateway_url: str | None = None
    gateway_token: str | None = None
    gateway_main_session_key: str | None = None


class GatewaysStatusResponse(SQLModel):
    connected: bool
    gateway_url: str
    sessions_count: int | None = None
    sessions: list[object] | None = None
    main_session_key: str | None = None
    main_session: object | None = None
    main_session_error: str | None = None
    error: str | None = None


class GatewaySessionsResponse(SQLModel):
    sessions: list[object]
    main_session_key: str | None = None
    main_session: object | None = None


class GatewaySessionResponse(SQLModel):
    session: object


class GatewaySessionHistoryResponse(SQLModel):
    history: list[object]


class GatewayCommandsResponse(SQLModel):
    protocol_version: int
    methods: list[str]
    events: list[str]
