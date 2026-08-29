from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.tasks.model import PriorityTier


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None


class TaskCreate(TaskBase):
    priority: PriorityTier | None = None


class TaskUpdate(BaseModel):
    title: str = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    is_done: bool | None = None


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None
    user_id: int
    is_done: bool
    priority: PriorityTier | None
    create_time: datetime
    done_time: datetime | None
