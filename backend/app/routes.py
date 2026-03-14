"""
API routes and endpoints.
Defines how the API responds to different requests.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Capital
from typing import List

# Create a router for capital endpoints
router = APIRouter(
    prefix="/api/capitals",
    tags=["capitals"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models for request/response validation
from pydantic import BaseModel, Field
from datetime import datetime

class CapitalCreate(BaseModel):
    """Schema for updating a capital - all fields optional."""
    name: str = None
    country: str = None
    latitude: float = None
    longitude: float = None
    remarks: str = None
    active: bool = None

class CapitalResponse(BaseModel):
    """Schema for capital response."""
    id: int
    name: str
    country: str
    latitude: float
    longitude: float
    remarks: str = None
    created_at: datetime
    active: bool = true
    
    class Config:
        from_attributes = True  # For SQLAlchemy compatibility

# Routes

@router.get("/", response_model=List[CapitalResponse])
def get_all_capitals(db: Session = Depends(get_db)):
    """
    Get all capital cities.
    
    Returns:
        List of all capitals with GPS coordinates.
    """
    capitals = db.query(Capital).all()
    return capitals

@router.get("/{capital_id}", response_model=CapitalResponse)
def get_capital(capital_id: int, db: Session = Depends(get_db)):
    """
    Get a specific capital by ID.
    
    Args:
        capital_id: The ID of the capital
        
    Returns:
        Capital details
        
    Raises:
        HTTPException: 404 if capital not found
    """
    capital = db.query(Capital).filter(Capital.id == capital_id).first()
    if not capital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Capital with ID {capital_id} not found"
        )
    return capital

@router.post("/", response_model=CapitalResponse, status_code=status.HTTP_201_CREATED)
def create_capital(capital: CapitalCreate, db: Session = Depends(get_db)):
    """
    Create a new capital city.
    
    Args:
        capital: Capital data to create
        
    Returns:
        Created capital with ID
        
    Raises:
        HTTPException: 400 if capital already exists
    """
    # Check if capital already exists
    existing = db.query(Capital).filter(Capital.name == capital.name).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Capital '{capital.name}' already exists"
        )
    
    # Create new capital
    db_capital = Capital(
        name=capital.name,
        country=capital.country,
        latitude=capital.latitude,
        longitude=capital.longitude,
        remarks=capital.remarks,
    )
    db.add(db_capital)
    db.commit()
    db.refresh(db_capital)
    return db_capital

@router.put("/{capital_id}", response_model=CapitalResponse)
def update_capital(capital_id: int, capital: CapitalUpdate, db: Session = Depends(get_db)):
    db_capital = db.query(Capital).filter(Capital.id == capital_id).first()
    if not db_capital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Capital with ID {capital_id} not found"
        )
    if capital.name is not None: db_capital.name = capital.name
    if capital.country is not None: db_capital.country = capital.country
    if capital.latitude is not None: db_capital.latitude = capital.latitude
    if capital.longitude is not None: db_capital.longitude = capital.longitude
    if capital.remarks is not None: db_capital.remarks = capital.remarks
    if capital.active is not None: db_capital.active = capital.active
    db.commit()
    db.refresh(db_capital)
    return db_capital,

@router.delete("/{capital_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_capital(capital_id: int, db: Session = Depends(get_db)):
    """
    Delete a capital.
    
    Args:
        capital_id: ID of capital to delete
        
    Raises:
        HTTPException: 404 if capital not found
    """
    db_capital = db.query(Capital).filter(Capital.id == capital_id).first()
    if not db_capital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Capital with ID {capital_id} not found"
        )
    
    db.delete(db_capital)
    db.commit()