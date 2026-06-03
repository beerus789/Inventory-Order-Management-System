"""Dashboard API routes."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from .dashboard_response import DashboardSummaryResponse
from .dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummaryResponse)
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get dashboard summary with key metrics."""
    service = DashboardService(db)
    summary = service.get_summary()
    return DashboardSummaryResponse(**summary)
