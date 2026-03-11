from app.database import engine, init_db
from app.config import settings

print(f"Connecting to: {settings.DATABASE_URL}")

try:
    with engine.connect() as connection:
        print("Database connection successful!")
        init_db()
except Exception as e:
    print(f"Connection failed: {e}")
    print("Make sure PostgreSQL is running:")
    print("  docker ps | grep gps-gis-postgres")