from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# --- Auth ---
class LoginRequest(BaseModel):
    password: str


class LoginResponse(BaseModel):
    token: str
    role: str


# --- Category ---
class CategoryOut(BaseModel):
    name: str
    display_name: str


# --- Donation Intake ---
class DonationItemOut(BaseModel):
    id: str
    intake_time: datetime
    intake_person: str
    category: str
    quantity: int
    notes: Optional[str] = ""
    photo_path: Optional[str] = None

    class Config:
        from_attributes = True


# --- Outbound ---
class OutboundCreate(BaseModel):
    outbound_person: str
    category: str
    quantity: int = 1
    notes: Optional[str] = ""


class OutboundOut(BaseModel):
    id: str
    outbound_time: datetime
    outbound_person: str
    category: str
    quantity: int
    notes: Optional[str] = ""

    class Config:
        from_attributes = True


# --- Reports ---
class CategorySummary(BaseModel):
    category: str
    display_name: str
    intake_total: int
    outbound_total: int
    net: int


class LowInventoryWarning(BaseModel):
    category: str
    display_name: str
    intake_14d: int
    outbound_14d: int
    deficit: int
    threshold: int
