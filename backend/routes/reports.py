import csv
import io
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import DonationItem, OutboundRecord, Category
from ..schemas import CategorySummary, LowInventoryWarning
from ..deps import require_auth, require_staff

router = APIRouter(prefix="/api/reports", tags=["reports"])


@router.get("/summary", response_model=list[CategorySummary])
def summary(
    days: int = Query(7, ge=1, le=365),
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth),
):
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    categories = db.query(Category).all()
    results = []
    for cat in categories:
        intake_total = (
            db.query(func.coalesce(func.sum(DonationItem.quantity), 0))
            .filter(DonationItem.category == cat.name, DonationItem.intake_time >= cutoff)
            .scalar()
        )
        outbound_total = (
            db.query(func.coalesce(func.sum(OutboundRecord.quantity), 0))
            .filter(OutboundRecord.category == cat.name, OutboundRecord.outbound_time >= cutoff)
            .scalar()
        )
        results.append(CategorySummary(
            category=cat.name,
            display_name=cat.display_name,
            intake_total=intake_total,
            outbound_total=outbound_total,
            net=intake_total - outbound_total,
        ))
    return results


@router.get("/cumulative", response_model=list[CategorySummary])
def cumulative(
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth),
):
    categories = db.query(Category).all()
    results = []
    for cat in categories:
        intake_total = (
            db.query(func.coalesce(func.sum(DonationItem.quantity), 0))
            .filter(DonationItem.category == cat.name)
            .scalar()
        )
        outbound_total = (
            db.query(func.coalesce(func.sum(OutboundRecord.quantity), 0))
            .filter(OutboundRecord.category == cat.name)
            .scalar()
        )
        results.append(CategorySummary(
            category=cat.name,
            display_name=cat.display_name,
            intake_total=intake_total,
            outbound_total=outbound_total,
            net=intake_total - outbound_total,
        ))
    return results


@router.get("/low-inventory", response_model=list[LowInventoryWarning])
def low_inventory(
    window: int = Query(14, ge=1, le=90),
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth),
):
    cutoff = datetime.now(timezone.utc) - timedelta(days=window)
    categories = db.query(Category).all()
    warnings = []
    for cat in categories:
        intake = (
            db.query(func.coalesce(func.sum(DonationItem.quantity), 0))
            .filter(DonationItem.category == cat.name, DonationItem.intake_time >= cutoff)
            .scalar()
        )
        outbound = (
            db.query(func.coalesce(func.sum(OutboundRecord.quantity), 0))
            .filter(OutboundRecord.category == cat.name, OutboundRecord.outbound_time >= cutoff)
            .scalar()
        )
        deficit = outbound - intake
        if deficit > cat.low_stock_threshold:
            warnings.append(LowInventoryWarning(
                category=cat.name,
                display_name=cat.display_name,
                intake_14d=intake,
                outbound_14d=outbound,
                deficit=deficit,
                threshold=cat.low_stock_threshold,
            ))
    return sorted(warnings, key=lambda w: w.deficit, reverse=True)


@router.get("/export.csv")
def export_csv(
    type: str = Query("intake", regex="^(intake|outbound)$"),
    db: Session = Depends(get_db),
    user: dict = Depends(require_staff),
):
    output = io.StringIO()
    writer = csv.writer(output)

    if type == "intake":
        writer.writerow(["id", "intake_time", "intake_person", "category", "quantity", "notes", "photo_path"])
        rows = db.query(DonationItem).order_by(DonationItem.intake_time.desc()).all()
        for r in rows:
            writer.writerow([r.id, r.intake_time, r.intake_person, r.category, r.quantity, r.notes, r.photo_path])
    else:
        writer.writerow(["id", "outbound_time", "outbound_person", "category", "quantity", "notes"])
        rows = db.query(OutboundRecord).order_by(OutboundRecord.outbound_time.desc()).all()
        for r in rows:
            writer.writerow([r.id, r.outbound_time, r.outbound_person, r.category, r.quantity, r.notes])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=goodsflow_{type}.csv"},
    )

from datetime import datetime, timedelta

@router.get("/activity")
def get_recent_activity(
    limit: int = 10,
    db: Session = Depends(get_db),
    user: dict = Depends(require_auth)
):
    """Get recent activity for Care Timeline - frontend compatible."""
    from ..models import DonationItem, OutboundRecord
    
    # Get recent intakes
    recent_intakes = db.query(DonationItem).order_by(
        DonationItem.intake_time.desc()
    ).limit(limit).all()
    
    # Get recent outbounds
    recent_outbounds = db.query(OutboundRecord).order_by(
        OutboundRecord.outbound_time.desc()
    ).limit(limit).all()
    
    # Combine and format for frontend
    events = []
    
    for intake in recent_intakes:
        item_desc = intake.item_name if intake.item_name else intake.category
        events.append({
            "id": f"i{intake.id}",
            "type": "donation",
            "title": f"{intake.quantity} {item_desc} added",
            "detail": f"Logged by {intake.intake_person}" + (f" · {intake.donor}" if intake.donor else ""),
            "time": format_time_ago(intake.intake_time),
            "timestamp": intake.intake_time.isoformat()
        })
    
    for outbound in recent_outbounds:
        events.append({
            "id": f"o{outbound.id}",
            "type": "distribution",
            "title": f"{outbound.quantity} {outbound.category} distributed",
            "detail": f"Logged by {outbound.outbound_person}",
            "time": format_time_ago(outbound.outbound_time),
            "timestamp": outbound.outbound_time.isoformat()
        })
    
    # Sort by timestamp, most recent first
    events.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return events[:limit]

def format_time_ago(dt: datetime) -> str:
    """Format datetime as '5 min ago', '2 hr ago', etc."""
    now = datetime.utcnow()
    diff = now - dt
    
    if diff < timedelta(minutes=1):
        return "Just now"
    elif diff < timedelta(hours=1):
        mins = int(diff.total_seconds() / 60)
        return f"{mins} min ago"
    elif diff < timedelta(days=1):
        hours = int(diff.total_seconds() / 3600)
        return f"{hours} hr ago"
    else:
        days = diff.days
        return f"{days} day{'s' if days > 1 else ''} ago"
