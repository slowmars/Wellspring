"""
Analytics endpoints that serve DS-generated insights - Frontend compatible format.
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
    """Get shortage urgency scores - frontend compatible format."""
    scores = recommendations.load_shortage_scores()
    
    # Transform to match frontend expectations
    result = []
    for item in scores:
        result.append({
            "key": item.get("category"),
            "label": item.get("display_name", item.get("category", "").title()),
            "status": item.get("urgency", "healthy").lower(),
            "urgencyScore": item.get("score", 0),
            "trend": item.get("trend", "Stable"),
            "recommendation": item.get("recommendation", ""),
            # Also include all original fields
            **item
        })
    
    return result

@router.get("/trends")
def get_trends(days: int = Query(30, ge=7, le=90)) -> List[Dict[str, Any]]:
    """Get trend analysis for intake/outbound patterns."""
    return recommendations.load_trends(days)

@router.get("/recommendations")
def get_recommendations() -> List[Dict[str, Any]]:
    """Get recommendations - frontend compatible format."""
    recs = recommendations.load_recommendations()
    
    # Transform priority: 1 → 'High', 2 → 'Medium', 3+ → 'Low'
    result = []
    for idx, rec in enumerate(recs):
        priority_num = rec.get("priority", 3)
        priority_str = "High" if priority_num == 1 else ("Medium" if priority_num == 2 else "Low")
        
        result.append({
            "id": f"r{idx+1}",
            "category": rec.get("category", "").title(),
            "priority": priority_str,
            "action": rec.get("action", ""),
            "reason": rec.get("reason", ""),
            # Include all original fields too
            **rec
        })
    
    return result

@router.get("/weekly-summary")
def get_weekly_summary(db: Session = Depends(get_db)):
    """Generate AI-powered weekly summary."""
    return generate_weekly_summary(db)
