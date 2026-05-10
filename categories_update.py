# Read the file
with open('backend/main.py', 'r') as f:
    content = f.read()

# Find and replace the categories endpoint
old_endpoint = '''@app.get("/api/categories")
def list_categories(db: Session = Depends(get_db)):
    """Get all donation categories"""
    cats = db.query(Category).all()
    return [{"name": c.name, "display_name": c.display_name} for c in cats]'''

new_endpoint = '''@app.get("/api/categories")
def list_categories(db: Session = Depends(get_db)):
    """Get all donation categories - frontend compatible format"""
    cats = db.query(Category).all()
    return [
        {
            "key": c.name,              # Frontend uses 'key'
            "label": c.display_name,    # Frontend uses 'label'
            "name": c.name              # Also keep 'name' for compatibility
        }
        for c in cats
    ]'''

content = content.replace(old_endpoint, new_endpoint)

# Write back
with open('backend/main.py', 'w') as f:
    f.write(content)

print("✅ Updated categories endpoint")
