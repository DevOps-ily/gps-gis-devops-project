"""
Database connection and session management.
Handles SQLAlchemy setup and session creation.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.config import settings

# Create database engine
# The engine is the core interface to the database
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQLALCHEMY_ECHO,  # Print SQL queries if DEBUG
    pool_pre_ping=True,  # Test connections before using them
    pool_recycle=3600,  # Recycle connections every hour
)

# Create session factory
# Sessions are used to interact with the database
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Session:
    """
    Dependency function to get database session.
    
    Usage in routes:
        @app.get("/capitals")
        def get_capitals(db: Session = Depends(get_db)):
            ...
    
    Yields:
        Session: Database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create all tables
def init_db():
    """Create all database tables from models."""
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created!")

# Function to drop all tables (be careful!)
def drop_db():
    """Drop all database tables. WARNING: Deletes all data!"""
    from app.models import Base
    Base.metadata.drop_all(bind=engine)
    print("⚠️  Database tables dropped!")