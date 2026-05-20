from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.todo import TodoCreateRequest, TodoResponse, TodoUpdateRequest
from app.services.todo import create_todo, delete_todo, get_user_todos, update_todo

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create(
    payload: TodoCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_todo(db, payload, current_user.id)


@router.get("", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def list_todos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_user_todos(db, current_user.id)


@router.put("/{todo_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update(
    todo_id: int,
    payload: TodoUpdateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_todo(db, todo_id, payload, current_user.id)


@router.delete("/{todo_id}", status_code=status.HTTP_200_OK)
def delete(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    delete_todo(db, todo_id, current_user.id)
    return {"detail": "Todo deleted successfully"}
