from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional
import os
from ..database import get_db
from ..models import DonationItem
from ..deps import require_auth

router = APIRouter(prefix="/api/intake", tags=["intake"])

@router.post("")
def create_intake(
    category: str = Form(...),
    quantity: int = Form(...),
    intake_person: str = Form(...),
    notes: Optional[str] = Form(None),
    photo: Optional[UploadFile] = File(None),
    # NEW FIELDS FROM FRONTEND:
    item_name: Optional[str] = Form(None),
    condition: Optional[str] = Form(None),
    donor: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth)
):
    """Create new intake/donation record with frontend-compatible fields."""
    
    # Validate category
    valid_categories = ["hygiene", "clothing", "baby", "food", "household", "emergency", "other"]
    if category not in valid_categories:
        raise HTTPException(status_code=400, detail=f"Invalid category. Must be one of: {valid_categories}")
    
    # Handle photo upload
    photo_path = None
    if photo:
        os.makedirs("uploads", exist_ok=True)
        photo_path = f"uploads/{datetime.utcnow().timestamp()}_{photo.filename}"
        with open(photo_path, "wb") as f:
            f.write(photo.file.read())
    
    # Create donation item with ALL fields
    item = DonationItem(
        category=category,
        quantity=quantity,
        intake_person=intake_person,
        notes=notes,
        photo_path=photo_path,
        item_name=item_name,
        condition=condition,
        donor=donor,
        intake_time=datetime.utcnow()
    )
    
    db.add(item)
    db.commit()
    db.refresh(item)
    
    return {
        "id": item.id,
        "category": item.category,
        "quantity": item.quantity,
        "intake_time": item.intake_time.isoformat(),
        "intake_person": item.intake_person,
        "notes": item.notes,
        "photo_path": item.photo_path,
        "item_name": item.item_name,
        "condition": item.condition,
        "donor": item.donor
    }

@router.get("")
def get_intake_list(
    limit: int = 50,
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth)
):
    """Get recent intake records."""
    items = db.query(DonationItem).order_by(
        DonationItem.intake_time.desc()
    ).limit(limit).all()
    
    return [
        {
            "id": item.id,
            "category": item.category,
            "quantity": item.quantity,
            "intake_time": item.intake_time.isoformat(),
            "intake_person": item.intake_person,
            "notes": item.notes,
            "photo_path": item.photo_path,
            "item_name": item.item_name,
            "condition": item.condition,
            "donor": item.donor
        }
        for item in items
    ]
