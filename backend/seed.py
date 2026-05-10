from datetime import datetime, timedelta, timezone
import random
from .database import SessionLocal
from .models import Category, DonationItem, OutboundRecord, new_uuid

CATEGORIES = [
    ("hygiene", "Hygiene", 5),
    ("clothing", "Clothing", 8),
    ("food", "Food & Snacks", 10),
    ("kids", "Kids & Baby", 5),
    ("misc", "Miscellaneous", 3),
]

DEMO_NAMES_IN = ["Maria L.", "Jose R.", "Aisha K.", "Sam T.", "Priya D."]
DEMO_NAMES_OUT = ["Front Desk", "Case Worker A", "Volunteer B", "Staff C"]

DEMO_NOTES_IN = [
    "Sealed, new condition",
    "Gently used, clean",
    "Donated by local church",
    "Bulk delivery from Target",
    "Community drive collection",
    "",
]
DEMO_NOTES_OUT = [
    "Family of 4",
    "Single mother, 2 kids",
    "Walk-in client",
    "Emergency request",
    "Scheduled pickup",
    "",
]


def seed_categories(db):
    existing = db.query(Category).count()
    if existing > 0:
        return
    for name, display, thresh in CATEGORIES:
        db.add(Category(name=name, display_name=display, low_stock_threshold=thresh))
    db.commit()


def seed_demo_data(db):
    existing = db.query(DonationItem).count()
    if existing > 0:
        return

    now = datetime.now(timezone.utc)
    cats = [c[0] for c in CATEGORIES]

    # Generate ~30 intake records over last 20 days
    for i in range(30):
        days_ago = random.randint(0, 20)
        cat = random.choice(cats)
        qty = random.randint(1, 20)
        # Make hygiene intake deliberately low for "low inventory" demo
        if cat == "hygiene":
            qty = random.randint(1, 3)
        db.add(DonationItem(
            id=new_uuid(),
            intake_time=now - timedelta(days=days_ago, hours=random.randint(0, 12)),
            intake_person=random.choice(DEMO_NAMES_IN),
            category=cat,
            quantity=qty,
            notes=random.choice(DEMO_NOTES_IN),
        ))

    # Generate ~20 outbound records over last 20 days
    for i in range(20):
        days_ago = random.randint(0, 20)
        cat = random.choice(cats)
        qty = random.randint(1, 10)
        # Make hygiene outbound deliberately high
        if cat == "hygiene":
            qty = random.randint(5, 15)
        db.add(OutboundRecord(
            id=new_uuid(),
            outbound_time=now - timedelta(days=days_ago, hours=random.randint(0, 12)),
            outbound_person=random.choice(DEMO_NAMES_OUT),
            category=cat,
            quantity=qty,
            notes=random.choice(DEMO_NOTES_OUT),
        ))

    db.commit()


def run_seed():
    db = SessionLocal()
    try:
        seed_categories(db)
        seed_demo_data(db)
    finally:
        db.close()
