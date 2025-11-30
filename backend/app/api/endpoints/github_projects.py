"""
GitHub Projects API endpoints
Author: Polo (林鴻全)
Date: 2025-11-30
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.publication import GithubProject
from app.schemas.publication import GithubProjectCreate, GithubProjectUpdate, GithubProjectResponse

router = APIRouter()


@router.get("/", response_model=List[GithubProjectResponse])
def get_github_projects(db: Session = Depends(get_db)):
    """Get all GitHub projects"""
    github_projects = db.query(GithubProject).order_by(GithubProject.display_order).all()
    return github_projects


@router.get("/{github_project_id}", response_model=GithubProjectResponse)
def get_github_project(github_project_id: int, db: Session = Depends(get_db)):
    """Get a specific GitHub project"""
    github_project = db.query(GithubProject).filter(GithubProject.id == github_project_id).first()
    if not github_project:
        raise HTTPException(status_code=404, detail="GitHub project not found")
    return github_project


@router.post("/", response_model=GithubProjectResponse)
def create_github_project(github_project: GithubProjectCreate, db: Session = Depends(get_db)):
    """Create a new GitHub project"""
    db_github_project = GithubProject(**github_project.dict())
    db.add(db_github_project)
    db.commit()
    db.refresh(db_github_project)
    return db_github_project


@router.put("/{github_project_id}", response_model=GithubProjectResponse)
def update_github_project(github_project_id: int, github_project: GithubProjectUpdate, db: Session = Depends(get_db)):
    """Update a GitHub project"""
    db_github_project = db.query(GithubProject).filter(GithubProject.id == github_project_id).first()
    if not db_github_project:
        raise HTTPException(status_code=404, detail="GitHub project not found")

    for key, value in github_project.dict(exclude_unset=True).items():
        setattr(db_github_project, key, value)

    db.commit()
    db.refresh(db_github_project)
    return db_github_project


@router.delete("/{github_project_id}")
def delete_github_project(github_project_id: int, db: Session = Depends(get_db)):
    """Delete a GitHub project"""
    db_github_project = db.query(GithubProject).filter(GithubProject.id == github_project_id).first()
    if not db_github_project:
        raise HTTPException(status_code=404, detail="GitHub project not found")

    db.delete(db_github_project)
    db.commit()
    return {"message": "GitHub project deleted successfully"}
