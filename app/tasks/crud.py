from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.tasks.model import PriorityTier, Task
from app.tasks.schemas import TaskCreate, TaskUpdate


def naive_utc(dt: datetime | None) -> datetime | None:
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


async def create_task(db: AsyncSession, task_data: TaskCreate, user_id: int) -> Task:
    deadline = naive_utc(task_data.deadline_date)

    task = Task(
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        deadline_date=deadline,
        user_id=user_id,
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
) -> Task | None:
    task = await get_task_by_id(db, user_id, task_id)

    if task is None:
        return None

    update_data = task_data.model_dump(exclude_unset=True)

    if "is_done" in update_data:
        task.is_done = update_data["is_done"]
        task.done_time = naive_utc(datetime.now(UTC)) if task.is_done else None
        del update_data["is_done"]

    if "deadline_date" in update_data:
        update_data["deadline_date"] = naive_utc(update_data["deadline_date"])

    for field, value in update_data.items():
        setattr(task, field, value)

    await db.commit()
    await db.refresh(task)

    return task


async def get_task_by_id(db: AsyncSession, user_id: int, task_id: int) -> Task | None:
    result = await db.execute(
        select(Task).where(Task.id == task_id, Task.user_id == user_id)
    )

    return result.scalar_one_or_none()


async def get_tasks_by_user(
    db: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    is_done: bool | None = None,
    priority: PriorityTier | None = None,
) -> list[Task]:
    result = await db.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.create_time.desc())
        .offset(skip)
        .limit(limit)
    )

    query = select(Task).where(Task.user_id == user_id)
    if is_done is not None:
        query = query.where(Task.is_done == is_done)
    if priority is not None:
        query = query.where(Task.priority == priority)
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)

    return result.scalars().all()


async def delete_task(db: AsyncSession, task_id: int, user_id: int) -> bool:
    task = await get_task_by_id(db, user_id, task_id)

    if task is None:
        return False

    await db.delete(task)
    await db.commit()

    return True
