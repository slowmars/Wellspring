from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import OutboundRecord, new_uuid
from ..schemas import OutboundCreate, OutboundOut
from ..deps import require_auth

router = APIRouter(prefix="/api/outbound", tags=["outbound"])


@router.post("", response_model=OutboundOut)
def create_outbound(
    data: OutboundCreate,
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth),
):
    record = OutboundRecord(
        id=new_uuid(),
        outbound_person=data.outbound_person,
        category=data.category,
        quantity=data.quantity,
        notes=data.notes,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.get("", response_model=list[OutboundOut])
def list_outbound(
    limit: int = 50,
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth),
):
    return (
        db.query(OutboundRecord)
        .order_by(OutboundRecord.outbound_time.desc())
        .limit(limit)
        .all()
    )
