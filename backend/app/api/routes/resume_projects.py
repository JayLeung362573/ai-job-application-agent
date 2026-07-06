from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.resume_project import ResumeProject
from app.schemas.resume_project import ResumeProjectRead


router = APIRouter(prefix="/resume-projects", tags=["resume-projects"])


@router.get("", response_model=list[ResumeProjectRead])
def list_resume_projects(db: Session = Depends(get_db)):
    statement = select(ResumeProject).order_by(ResumeProject.name)
    return db.scalars(statement).all()