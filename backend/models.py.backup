import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from .database import Base


def new_uuid():
    return str(uuid.uuid4())


def utcnow():
    return datetime.now(timezone.utc)


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False, index=True)
    display_name = Column(String(100), nullable=False)
    low_stock_threshold = Column(Integer, default=5)


class DonationItem(Base):
    __tablename__ = "donation_items"
    id = Column(String(36), primary_key=True, default=new_uuid)
    intake_time = Column(DateTime, default=utcnow, index=True)
    intake_person = Column(String(200), nullable=False)
    category = Column(String(50), ForeignKey("categories.name"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    notes = Column(Text, default="")
    photo_path = Column(String(500), default=None)


class OutboundRecord(Base):
    __tablename__ = "outbound_records"
    id = Column(String(36), primary_key=True, default=new_uuid)
    outbound_time = Column(DateTime, default=utcnow, index=True)
    outbound_person = Column(String(200), nullable=False)
    category = Column(String(50), ForeignKey("categories.name"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=1)
    notes = Column(Text, default="")
