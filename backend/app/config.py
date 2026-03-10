"""
Configuration management for the application.
Loads settings from environment variables.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://gps_user:gps_password@localhost:5432/gps_gis_db"
    )
    DATABASE_HOST: str = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_PORT: int = int(os.getenv("DATABASE_PORT", 5432))
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "gps_gis_db")
    DATABASE_USER: str = os.getenv("DATABASE_USER", "gps_user")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD", "gps_password")
    
    # FastAPI Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", 5000))
    API_ENV: str = os.getenv("API_ENV", "development")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # Computed values
    DEBUG: bool = API_ENV == "development"
    
    # SQLAlchemy Engine Configuration
    SQLALCHEMY_ECHO: bool = DEBUG  # Print SQL queries in development
    
    def __repr__(self):
        return f"<Settings API_ENV={self.API_ENV} DATABASE={self.DATABASE_NAME}>"

# Create a single settings instance
settings = Settings()

# Print settings on startup (helpful for debugging)
if __name__ == "__main__":
    print(f"Settings loaded: {settings}")
EOF