import os
import uuid
from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..models import DonationItem, new_uuid
from ..schemas import DonationItemOut
from ..deps import require_auth

router = APIRouter(prefix="/api/intake", tags=["intake"])

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("", response_model=DonationItemOut)
async def create_intake(
    intake_person: str = Form(...),
    category: str = Form(...),
    quantity: int = Form(1),
    notes: str = Form(""),
    photo: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth),
):
    photo_path = None
    if photo and photo.filename:
        ext = os.path.splitext(photo.filename)[1] or ".jpg"
        filename = f"{uuid.uuid4()}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)
        content = await photo.read()
        with open(filepath, "wb") as f:
            f.write(content)
        photo_path = f"/uploads/{filename}"

    item = DonationItem(
        id=new_uuid(),
        intake_person=intake_person,
        category=category,
        quantity=quantity,
        notes=notes,
        photo_path=photo_path,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.get("", response_model=list[DonationItemOut])
def list_intake(
    limit: int = 50,
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth),
):
    return (
        db.query(DonationItem)
        .order_by(DonationItem.intake_time.desc())
        .limit(limit)
        .all()
    )
