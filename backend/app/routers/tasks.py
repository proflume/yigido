from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Task, Project, User
from app.schemas import TaskCreate, TaskUpdate, TaskRead
from app.security import get_current_user
from app.services import notify_task_change, notify_task_deleted


router = APIRouter()


@router.get("/", response_model=list[TaskRead])
def list_tasks(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tasks = (
        db.query(Task)
        .join(Project, Project.id == Task.project_id)
        .filter(Project.owner_id == current_user.id)
        .all()
    )
    return tasks


@router.post("/", response_model=TaskRead)
def create_task(task_in: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == task_in.project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    task = Task(project_id=task_in.project_id, title=task_in.title, description=task_in.description)
    db.add(task)
    db.commit()
    db.refresh(task)
    notify_task_change(task)
    return task


@router.patch("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: int, task_in: TaskUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    task = (
        db.query(Task)
        .join(Project, Project.id == Task.project_id)
        .filter(Task.id == task_id, Project.owner_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task_in.title is not None:
        task.title = task_in.title
    if task_in.description is not None:
        task.description = task_in.description
    if task_in.is_done is not None:
        task.is_done = task_in.is_done
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = (
        db.query(Task)
        .join(Project, Project.id == Task.project_id)
        .filter(Task.id == task_id, Project.owner_id == current_user.id)
        .first()
    )
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    notify_task_deleted(task_id)
    return {"ok": True}
