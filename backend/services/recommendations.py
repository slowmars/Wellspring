"""
Service layer for loading DS-generated analytics outputs.
Falls back gracefully if files don't exist yet.
"""
import os
import json
from typing import List, Dict, Any


# Path to DS outputs folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUTS_DIR = os.path.join(BASE_DIR, "data_science", "outputs")


def load_shortage_scores() -> List[Dict[str, Any]]:
    """
    Load shortage scores from DS output.
    
    Returns:
        [
            {
                "category": "hygiene",
                "display_name": "Hygiene",
                "score": 8.7,
                "urgency": "critical",
                "deficit_14d": 35,
                "burn_rate_per_day": 4.2,
                "days_until_empty": 3
            },
            ...
        ]
    
    Fallback: Returns empty list if file doesn't exist.
    """
    filepath = os.path.join(OUTPUTS_DIR, "shortage_scores.json")
    
    if not os.path.exists(filepath):
        print(f"[INFO] shortage_scores.json not found at {filepath} - returning empty list")
        return []
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"[INFO] Loaded {len(data)} shortage scores from DS outputs")
        return data
    except Exception as e:
        print(f"[ERROR] Failed to load shortage_scores.json: {e}")
        return []


def load_trends(days: int = 30) -> List[Dict[str, Any]]:
    """
    Load trend analysis from DS output.
    
    Returns:
        [
            {
                "category": "hygiene",
                "trend": "decreasing",
                "change_pct": -12.5
            },
            ...
        ]
    
    Note: `days` parameter is for API compatibility but currently ignored.
    DS student controls the lookback window.
    """
    filepath = os.path.join(OUTPUTS_DIR, "trends.json")
    
    if not os.path.exists(filepath):
        print(f"[INFO] trends.json not found - returning empty list")
        return []
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"[INFO] Loaded {len(data)} trends from DS outputs")
        return data
    except Exception as e:
        print(f"[ERROR] Failed to load trends.json: {e}")
        return []


def load_recommendations() -> List[Dict[str, Any]]:
    """
    Load actionable recommendations from DS output.
    
    Returns:
        [
            {
                "category": "hygiene",
                "action": "Request 50+ items ASAP",
                "reason": "Outbound exceeds intake by 35 units",
                "priority": 1,
                "confidence": 0.92
            },
            ...
        ]
    """
    filepath = os.path.join(OUTPUTS_DIR, "recommendations.json")
    
    if not os.path.exists(filepath):
        print(f"[INFO] recommendations.json not found - returning empty list")
        return []
    
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"[INFO] Loaded {len(data)} recommendations from DS outputs")
        return data
    except Exception as e:
        print(f"[ERROR] Failed to load recommendations.json: {e}")
        return []
