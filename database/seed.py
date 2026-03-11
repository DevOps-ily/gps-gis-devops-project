"""
Seed script to populate database with initial data.
Adds 5 capital cities with GPS coordinates.
"""

import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.database import SessionLocal, init_db
from app.models import Capital

def seed_data():
    """Populate database with 5 capital cities."""
    
    # Initialize database tables
    init_db()
    
    # Get database session
    db = SessionLocal()
    
    # Check if data already exists
    existing_capitals = db.query(Capital).count()
    if existing_capitals >= 999:
        print(f"⚠️  Database already has {existing_capitals} capitals. Skipping seed.")
        db.close()
        return
    
    # 5 Capital cities with GPS coordinates
    capitals_data = [
        {
            "name": "Paris",
            "country": "France",
            "latitude": 48.8566,
            "longitude": 2.3522,
            "remarks": "Europe, Mainland"
        },
        {
            "name": "Prague",
            "country": "Czechia",
            "latitude": 50.0755,
            "longitude": 14.4378,
            "remarks": "Europe, Mainland"
        },
        {
            "name": "Ulaanbaatar",
            "country": "Mongolia",
            "latitude": 47.9084,
            "longitude": 106.8855,
            "remarks": "Asia, Mainland"
        },
        {
            "name": "Thimphu",
            "country": "Bhutan",
            "latitude": 27.5142,
            "longitude": 89.6386,
            "remarks": "Asia, Mainland, Himalayan"
        },
        {
            "name": "Malé",
            "country": "Maldives",
            "latitude": 4.1755,
            "longitude": 73.5093,
            "remarks": "Asia, Island, Indian Ocean"
        },
        {
            "name": "Tokyo",
            "country": "Japan",
            "latitude": 35.6762,
            "longitude": 139.6503,
            "remarks": "Asia, Mainland, Island Nation"
        },
        {
            "name": "Oslo",
            "country": "Norway",
            "latitude": 59.9139,
            "longitude": 10.7522,
            "remarks": "Europe, Mainland"
        },
        {
            "name": "Canberra",
            "country": "Australia",
            "latitude": -35.2809,
            "longitude": 149.1300,
            "remarks": "Oceania, Mainland"
        },
        {
            "name": "PointNo677",
            "country": "WORLD",
            "latitude": 32.73402781272827,
            "longitude": 50.736990323581786,
            "remarks": "Zayanderud Dam, Iran, Mainland"
        }
    ]
    
    # Add each capital to database
    for capital_data in capitals_data:
        capital = Capital(**capital_data)
        db.add(capital)
        print(f"✅ Added: {capital_data['name']}, {capital_data['country']}")
    
    # Commit all changes
    db.commit()
    
    # Verify data was inserted
    count = db.query(Capital).count()
    print(f"\n✅ Seed complete! Total capitals in database: {count}")
    
    # Display all capitals
    all_capitals = db.query(Capital).all()
    print("\n📍 Capitals in database:")
    for cap in all_capitals:
        print(f"  - {cap.name} ({cap.country}): {cap.latitude}, {cap.longitude}")
    
    db.close()

if __name__ == "__main__":
    try:
        seed_data()
    except Exception as e:
        print(f"❌ Seeding failed: {e}")
        import traceback
        traceback.print_exc()