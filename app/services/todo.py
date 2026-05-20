from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.todo import GuestTodo, Todo
from app.schemas.todo import GuestTodoCreateRequest, TodoCreateRequest, TodoUpdateRequest


def create_todo(db: Session, payload: TodoCreateRequest, user_id: int) -> Todo:
    todo = Todo(title=payload.title, body=payload.body, user_id=user_id)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_user_todos(db: Session, user_id: int) -> list[Todo]:
    return db.query(Todo).filter(Todo.user_id == user_id).all()


def update_todo(db: Session, todo_id: int, payload: TodoUpdateRequest, user_id: int) -> Todo:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    if todo.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    if payload.title is not None:
        todo.title = payload.title
    if payload.body is not None:
        todo.body = payload.body
    if payload.status is not None:
        todo.status = payload.status

    todo.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo_id: int, user_id: int) -> None:
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")

    if todo.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    db.delete(todo)
    db.commit()


def create_guest_todo(db: Session, payload: GuestTodoCreateRequest) -> GuestTodo:
    todo = GuestTodo(title=payload.title, body=payload.body)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def get_all_guest_todos(db: Session) -> list[GuestTodo]:
    return db.query(GuestTodo).all()
