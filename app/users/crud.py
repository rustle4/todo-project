from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users.models import User

from .schemas import UserCreate


async def create_user(db: AsyncSession, user_data: UserCreate) -> User:
    db_user = User(
        username=user_data.username, email=user_data.email, password=user_data.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


async def get_user_by_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()
