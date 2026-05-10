from backend.database import engine, SessionLocal
from sqlalchemy import text

db = SessionLocal()

# Add missing categories
db.execute(text("INSERT OR IGNORE INTO categories (name, display_name) VALUES ('baby', 'Baby Supplies')"))
db.execute(text("INSERT OR IGNORE INTO categories (name, display_name) VALUES ('emergency', 'Emergency Kits')"))
db.commit()
db.close()

print("✅ Added baby and emergency categories")
