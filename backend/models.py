from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Category(Base):
    __tablename__ = "categories"
    name = Column(String, primary_key=True)
    display_name = Column(String, nullable=False)

class DonationItem(Base):
    __tablename__ = "donation_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, ForeignKey("categories.name"), nullable=False)
    quantity = Column(Integer, nullable=False)
    intake_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    intake_person = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
    photo_path = Column(String, nullable=True)
    
    # NEW FIELDS FOR FRONTEND COMPATIBILITY
    item_name = Column(String, nullable=True)
    condition = Column(String, nullable=True)
    donor = Column(String, nullable=True)

class OutboundRecord(Base):
    __tablename__ = "outbound_records"
    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, ForeignKey("categories.name"), nullable=False)
    quantity = Column(Integer, nullable=False)
    outbound_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    outbound_person = Column(String, nullable=False)
    notes = Column(Text, nullable=True)
