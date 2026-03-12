import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.database import SessionLocal
from app.models import Capital

db = SessionLocal()
db.query(Capital).delete()
db.commit()
print("Database cleared!")
db.close()