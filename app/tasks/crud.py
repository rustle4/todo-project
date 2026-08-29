from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.tasks import model
from app.tasks.schemas import TaskCreate, TaskUpdate


async def create_task(
    db: AsyncSession, task_data: TaskCreate, user_id: int
) -> model.Task:
    task = model.Task(
        title=task_data.title, description=task_data.description, user_id=user_id
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


async def update_task(
    db: AsyncSession,
    task_id: int,
    task_data: TaskUpdate,
    user_id: int,
) -> model.Task | None:
    task = await get_task_by_id(db, task_id, user_id)

    if task is None:
        return None

    update_data = task_data.model_dump(exclude_unset=True)

    if "is_done" in update_data:
        task.is_done = update_data["is_done"]
        task.done_time = datetime.now(UTC) if task.is_done else None
        del update_data["is_done"]

    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    return task


async def get_task_by_id(
    db: AsyncSession, user_id: int, task_id: int
) -> model.Task | None:
    result = await db.execute(
        select(model.Task).where(
            model.Task.id == task_id, model.Task.user_id == user_id
        )
    )

    return result.scalar_one_or_none()


async def get_tasks_by_user(
    db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100
) -> list[model.Task]:
    result = await db.execute(
        select(model.Task)
        .where(model.Task.user_id == user_id)
        .order_by(model.Task.create_time.desc())
        .offset(skip)
        .limit(limit)
    )

    return result.scalars().all()


async def delete_task(db: AsyncSession, task_id: int, user_id: int) -> bool:
    task = await get_task_by_id(db, task_id, user_id)

    if task is None:
        return False

    await db.delete(task)
    await db.commit()

    return True
