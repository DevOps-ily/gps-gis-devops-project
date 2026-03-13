import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app.database import SessionLocal, init_db
from app.models import Capital

init_db()
db = SessionLocal()

missing = [
    {"name": "Ulaanbaatar", "country": "Mongolia", "latitude": 47.9084, "longitude": 106.8855, "remarks": "Asia, Mainland"},
    {"name": "Thimphu", "country": "Bhutan", "latitude": 27.5142, "longitude": 89.6386, "remarks": "Asia, Mainland, Himalayan"},
    {"name": "Male", "country": "Maldives", "latitude": 4.1755, "longitude": 73.5093, "remarks": "Asia, Island, Indian Ocean"},
    {"name": "PointNo677", "country": "WORLD", "latitude": 32.73402781272827, "longitude": 50.736990323581786, "remarks": "Zayanderud Dam, Iran, Mainland"},
]

for m in missing:
    db.add(Capital(**m))
    print(f"Added: {m['name']}")

db.commit()
print("Done!")