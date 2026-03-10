"""
Main FastAPI application.
Entry point for the GPS/GIS API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import init_db
from app.routes import router

# Create FastAPI app instance
app = FastAPI(
    title="GPS/GIS Capital Cities API",
    description="API to manage GPS coordinates of world capital cities",
    version="1.0.0",
)

# Add CORS middleware (allows requests from different origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)

# Health check endpoint
@app.get("/health")
def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "environment": settings.API_ENV,
        "database": settings.DATABASE_NAME,
    }

# Root endpoint
@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to GPS/GIS Capital Cities API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "capitals": "/api/capitals",
            "docs": "/docs",
            "openapi": "/openapi.json",
        }
    }

# Startup event
@app.on_event("startup")
def startup_event():
    """Run on application startup."""
    print("🚀 Starting GPS/GIS API...")
    print(f"📊 Configuration: {settings}")
    try:
        init_db()
        print("✅ Database initialized!")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")

# Shutdown event
@app.on_event("shutdown")
def shutdown_event():
    """Run on application shutdown."""
    print("🛑 Shutting down GPS/GIS API...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.API_HOST,
        port=settings.API_PORT,
    )
EOF