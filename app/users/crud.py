from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.jwt_hash import get_password_hash
from app.users.model import User

from .schemas import UserCreate


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    db_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=get_password_hash(user_data.password),
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User | None:
    result = await db.execute(select(User).where(User.id == user_id))

    return result.scalar_one_or_none()


async def get_user_by_username(db: AsyncSession, useraname: str) -> User | None:
    result = await db.execute(select(User.username).where(User.username == useraname))

    return result.scalar_one_or_none()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User.email).where(User.email == email))

    return result.scalar_one_or_none()
