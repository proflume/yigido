from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Project, User
from app.schemas import ProjectCreate, ProjectRead
from app.security import get_current_user


router = APIRouter()


@router.get("/", response_model=list[ProjectRead])
def list_projects(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    projects = db.query(Project).filter(Project.owner_id == current_user.id).all()
    return projects


@router.post("/", response_model=ProjectRead)
def create_project(
    project_in: ProjectCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    project = Project(name=project_in.name, description=project_in.description, owner_id=current_user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


@router.delete("/{project_id}")
def delete_project(project_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    db.commit()
    return {"ok": True}
