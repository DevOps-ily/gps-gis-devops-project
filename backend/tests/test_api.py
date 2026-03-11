"""
Tests for the GPS/GIS API endpoints.
"""

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import our app
from app.main import app
from app.database import get_db, Base
from app.models import Capital

# Create in-memory test database
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

class TestHealth:
    def test_health_check(self):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

class TestRootEndpoint:
    def test_root(self):
        response = client.get("/")
        assert response.status_code == 200
        assert "message" in response.json()

class TestCapitals:
    def test_get_empty_capitals(self):
        response = client.get("/api/capitals")
        assert response.status_code == 200
        assert response.json() == []
    
    def test_create_capital(self):
        response = client.post(
            "/api/capitals",
            json={
                "name": "Paris",
                "country": "France",
                "latitude": 48.8566,
                "longitude": 2.3522,
                "remarks": "Europe"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Paris"
        assert data["id"] == 1
    
    def test_get_capitals(self):
        # First create a capital
        client.post(
            "/api/capitals",
            json={
                "name": "Paris",
                "country": "France",
                "latitude": 48.8566,
                "longitude": 2.3522,
                "remarks": "Europe"
            }
        )
        
        # Then get all capitals
        response = client.get("/api/capitals")
        assert response.status_code == 200
        assert len(response.json()) == 1
    
    def test_get_capital_by_id(self):
        # Create a capital
        create_response = client.post(
            "/api/capitals",
            json={
                "name": "Prague",
                "country": "Czechia",
                "latitude": 50.0755,
                "longitude": 14.4378,
                "remarks": "Europe"
            }
        )
        capital_id = create_response.json()["id"]
        
        # Get by ID
        response = client.get(f"/api/capitals/{capital_id}")
        assert response.status_code == 200
        assert response.json()["name"] == "Prague"
    
    def test_get_nonexistent_capital(self):
        response = client.get("/api/capitals/999")
        assert response.status_code == 404

if __name__ == "__main__":
    pytest.main([__file__, "-v"])