"""
Analytics endpoints that serve DS-generated insights.
"""
from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from ..deps import require_auth, get_db
from ..services import recommendations
from ..services.ai_assistant import generate_weekly_summary

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/test")
def test_analytics():
    """Test endpoint to verify analytics router is working"""
    return {"status": "analytics router working", "message": "Ready for DS integration"}

@router.get("/shortage-scores")
def get_shortage_scores() -> List[Dict[str, Any]]:
    """Get shortage urgency scores for all categories."""
    return recommendations.load_shortage_scores()

@router.get("/trends")
def get_trends(days: int = Query(30, ge=7, le=90)) -> List[Dict[str, Any]]:
    """Get trend analysis for intake/outbound patterns."""
    return recommendations.load_trends(days)

@router.get("/recommendations")
def get_recommendations() -> List[Dict[str, Any]]:
    """Get actionable recommendations based on shortage analysis."""
    return recommendations.load_recommendations()

@router.get("/weekly-summary")
def get_weekly_summary(db: Session = Depends(get_db)):
    """Generate AI-powered weekly summary."""
    return generate_weekly_summary(db)
