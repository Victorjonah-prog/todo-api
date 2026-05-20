from datetime import datetime

from pydantic import BaseModel

from app.models.todo import TodoStatus


class TodoCreateRequest(BaseModel):
    title: str
    body: str


class TodoUpdateRequest(BaseModel):
    title: str | None = None
    body: str | None = None
    status: TodoStatus | None = None


class TodoResponse(BaseModel):
    id: int
    user_id: int
    title: str
    body: str
    status: TodoStatus
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class GuestTodoCreateRequest(BaseModel):
    title: str
    body: str


class GuestTodoResponse(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime

    model_config = {"from_attributes": True}
