from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.todo import GuestTodoCreateRequest, GuestTodoResponse
from app.services.todo import create_guest_todo, get_all_guest_todos

router = APIRouter(prefix="/guest/todos", tags=["Guest Todos"])


@router.post("", response_model=GuestTodoResponse, status_code=status.HTTP_201_CREATED)
def create(payload: GuestTodoCreateRequest, db: Session = Depends(get_db)):
    return create_guest_todo(db, payload)


@router.get("", response_model=list[GuestTodoResponse], status_code=status.HTTP_200_OK)
def list_todos(db: Session = Depends(get_db)):
    return get_all_guest_todos(db)
