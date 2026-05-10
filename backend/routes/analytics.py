"""
Analytics endpoints that serve DS-generated insights.
"""
from fastapi import APIRouter, Depends, Query
from typing import List, Dict, Any

from ..deps import require_auth

router = APIRouter(prefix="/api/analytics", tags=["analytics"])


@router.get("/test")
def test_analytics():
    """Test endpoint to verify analytics router is working"""
    return {"status": "analytics router working", "message": "Ready for DS integration"}


@router.get("/shortage-scores")
def get_shortage_scores(
    user: dict = Depends(require_auth)
) -> List[Dict[str, Any]]:
    """
    Get shortage urgency scores for all categories.
    Returns empty list until DS student generates data.
    """
    # TODO: Will load from data_science/outputs/shortage_scores.json
    return []


@router.get("/trends")
def get_trends(
    days: int = Query(30, ge=7, le=90),
    user: dict = Depends(require_auth)
) -> List[Dict[str, Any]]:
    """
    Get trend analysis for intake/outbound patterns.
    Returns empty list until DS student generates data.
    """
    # TODO: Will load from data_science/outputs/trends.json
    return []


@router.get("/recommendations")
def get_recommendations(
    user: dict = Depends(require_auth)
) -> List[Dict[str, Any]]:
    """
    Get actionable recommendations based on shortage analysis.
    Returns empty list until DS student generates data.
    """
    # TODO: Will load from data_science/outputs/recommendations.json
    return []
