import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .seed import run_seed
from .models import Category
from .routes import auth, intake, outbound, reports, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: create tables and seed data"""
    Base.metadata.create_all(bind=engine)
    run_seed()
    yield


app = FastAPI(
    title="GoodsFlow API",
    version="2.0.0",
    description="Women's Center Donation Inventory API",
    lifespan=lifespan
)

# ============================================================
# CORS MIDDLEWARE (CRITICAL FOR VERCEL FRONTEND)
# ============================================================
ALLOWED_ORIGINS = [
    "http://localhost:3000",           # Local frontend dev
    "http://localhost:3001",           # Alternative port
    "https://*.vercel.app",            # All Vercel preview deployments
    # Add your specific Vercel URL when deployed:
    # "https://goodsflow.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For hackathon speed; tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# HEALTH CHECK ENDPOINT
# ============================================================
@app.get("/health")
def health_check():
    """Health check endpoint for monitoring and Fly.io"""
    return {
        "status": "healthy",
        "service": "GoodsFlow API",
        "version": "2.0.0"
    }


# ============================================================
# CATEGORIES ENDPOINT (public, no auth)
# ============================================================
@app.get("/api/categories")
def list_categories(db: Session = Depends(get_db)):
    """Get all donation categories"""
    cats = db.query(Category).all()
    return [{"name": c.name, "display_name": c.display_name} for c in cats]


# ============================================================
# INCLUDE ALL ROUTES
# ============================================================
app.include_router(auth.router)
app.include_router(intake.router)
app.include_router(outbound.router)
app.include_router(reports.router)
app.include_router(analytics.router)  # NEW

# ============================================================
# SERVE UPLOADED PHOTOS
# ============================================================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
uploads_dir = os.path.join(BASE_DIR, "uploads")
os.makedirs(uploads_dir, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")


# ============================================================
# ROOT ENDPOINT
# ============================================================
@app.get("/")
def root():
    """API root — redirect to /docs for interactive documentation"""
    return {
        "message": "GoodsFlow API",
        "docs": "/docs",
        "health": "/health"
    }