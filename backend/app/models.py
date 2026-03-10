"""
Database models using SQLAlchemy ORM.
Defines the structure of tables in the database.
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Base class for all models
Base = declarative_base()

class Capital(Base):
    """
    Capital city model.
    
    Represents one capital city with GPS coordinates and metadata.
    
    Attributes:
        id: Unique identifier (primary key)
        name: Name of the capital city
        country: Country name
        latitude: GPS latitude coordinate
        longitude: GPS longitude coordinate
        remarks: Additional information (e.g., "Island", "Mainland", "Asia")
        created_at: Timestamp when record was created
    """
    
    __tablename__ = "capitals"
    
    # Columns definition
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True, nullable=False)
    country = Column(String(100), nullable=False, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    remarks = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f"<Capital(id={self.id}, name={self.name}, country={self.country})>"
    
    def to_dict(self):
        """Convert model to dictionary for JSON responses."""
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "remarks": self.remarks,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
EOF