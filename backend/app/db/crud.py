from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from sqlalchemy.exc import IntegrityError
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

ModelT = TypeVar("ModelT", bound=SQLModel)


class DoesNotExist(LookupError):
    pass


class MultipleObjectsReturned(LookupError):
    pass


async def get_by_id(session: AsyncSession, model: type[ModelT], obj_id: Any) -> ModelT | None:
    return await session.get(model, obj_id)


async def get(session: AsyncSession, model: type[ModelT], **lookup: Any) -> ModelT:
    stmt = select(model)
    for key, value in lookup.items():
        stmt = stmt.where(getattr(model, key) == value)
    stmt = stmt.limit(2)
    items = (await session.exec(stmt)).all()
    if not items:
        raise DoesNotExist(f"{model.__name__} matching query does not exist.")
    if len(items) > 1:
        raise MultipleObjectsReturned(
            f"Multiple {model.__name__} objects returned for lookup {lookup!r}."
        )
    return items[0]


async def get_one_by(session: AsyncSession, model: type[ModelT], **lookup: Any) -> ModelT | None:
    stmt = select(model)
    for key, value in lookup.items():
        stmt = stmt.where(getattr(model, key) == value)
    return (await session.exec(stmt)).first()


async def create(
    session: AsyncSession,
    model: type[ModelT],
    *,
    commit: bool = True,
    refresh: bool = True,
    **data: Any,
) -> ModelT:
    obj = model.model_validate(data)
    session.add(obj)
    await session.flush()
    if commit:
        await session.commit()
    if refresh:
        await session.refresh(obj)
    return obj


async def save(
    session: AsyncSession,
    obj: ModelT,
    *,
    commit: bool = True,
    refresh: bool = True,
) -> ModelT:
    session.add(obj)
    await session.flush()
    if commit:
        await session.commit()
    if refresh:
        await session.refresh(obj)
    return obj


async def delete(session: AsyncSession, obj: ModelT, *, commit: bool = True) -> None:
    await session.delete(obj)
    if commit:
        await session.commit()


async def get_or_create(
    session: AsyncSession,
    model: type[ModelT],
    *,
    defaults: Mapping[str, Any] | None = None,
    commit: bool = True,
    refresh: bool = True,
    **lookup: Any,
) -> tuple[ModelT, bool]:
    stmt = select(model)
    for key, value in lookup.items():
        stmt = stmt.where(getattr(model, key) == value)

    existing = (await session.exec(stmt)).first()
    if existing is not None:
        return existing, False

    payload: dict[str, Any] = dict(lookup)
    if defaults:
        for key, value in defaults.items():
            payload.setdefault(key, value)

    obj = model.model_validate(payload)
    session.add(obj)
    try:
        await session.flush()
        if commit:
            await session.commit()
    except IntegrityError:
        # If another concurrent request inserted the same unique row, surface that row.
        await session.rollback()
        existing = (await session.exec(stmt)).first()
        if existing is not None:
            return existing, False
        raise

    if refresh:
        await session.refresh(obj)
    return obj, True
