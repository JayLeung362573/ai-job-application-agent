import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.application import Application, ApplicationStatus
from app.schemas.application import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationUpdate,
)

from app.api.dependencies import get_analysis_service
from app.schemas.analysis import AnalysisRead
from app.services.analysis import (
    AnalysisNotFoundError,
    AnalysisService,
    ApplicationNotFoundError,
)


router = APIRouter(prefix="/applications", tags=["applications"])


@router.post(
    "",
    response_model=ApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_application(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db),
):
    application = Application(**application_data.model_dump())

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@router.get("", response_model=list[ApplicationRead])
def list_applications(
    q: Annotated[
        str | None,
        Query(
            min_length=1,
            max_length=100,
            description="Search company, title, location, description, or notes",
        ),
    ] = None,
    application_status: Annotated[
        ApplicationStatus | None,
        Query(
            alias="status",
            description="Filter applications by status",
        ),
    ] = None,
    db: Session = Depends(get_db),
):
    statement = select(Application)

    if application_status is not None:
        statement = statement.where(
            Application.status == application_status
        )

    if q is not None:
        search_term = q.strip()

        if search_term:
            search_pattern = f"%{search_term}%"

            statement = statement.where(
                or_(
                    Application.company.ilike(search_pattern),
                    Application.title.ilike(search_pattern),
                    Application.location.ilike(search_pattern),
                    Application.job_description.ilike(search_pattern),
                    Application.notes.ilike(search_pattern),
                )
            )

    statement = statement.order_by(Application.updated_at.desc())

    return db.scalars(statement).all()

@router.post(
    "/{application_id}/analyze",
    response_model=AnalysisRead,
    status_code=status.HTTP_201_CREATED,
)
def analyze_application(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    analysis_service: AnalysisService = Depends(
        get_analysis_service
    ),
):
    try:
        return analysis_service.analyze_application(
            db=db,
            application_id=application_id,
        )
    except ApplicationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        ) from exc

@router.get(
    "/{application_id}/analysis",
    response_model=AnalysisRead,
)
def get_latest_application_analysis(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
    analysis_service: AnalysisService = Depends(
        get_analysis_service
    ),
):
    try:
        return analysis_service.get_latest_analysis(
            db=db,
            application_id=application_id,
        )
    except ApplicationNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        ) from exc
    except AnalysisNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Analysis not found",
        ) from exc

@router.get("/{application_id}", response_model=ApplicationRead)
def get_application(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    application = db.get(Application, application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    return application

@router.patch("/{application_id}", response_model=ApplicationRead)
def update_application(
    application_id: uuid.UUID,
    application_data: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    application = db.get(Application, application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    update_data = application_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return application

@router.delete(
    "/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_application(
    application_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    application = db.get(Application, application_id)

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found",
        )

    db.delete(application)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)