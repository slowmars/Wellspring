from backend.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    # Add new columns
    try:
        conn.execute(text("ALTER TABLE donation_items ADD COLUMN item_name TEXT"))
        print("✅ Added item_name column")
    except:
        print("⚠️  item_name column already exists")
    
    try:
        conn.execute(text("ALTER TABLE donation_items ADD COLUMN condition TEXT"))
        print("✅ Added condition column")
    except:
        print("⚠️  condition column already exists")
    
    try:
        conn.execute(text("ALTER TABLE donation_items ADD COLUMN donor TEXT"))
        print("✅ Added donor column")
    except:
        print("⚠️  donor column already exists")
    
    conn.commit()

print("✅ Database migration complete")
