from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, videos, projects
import os

app = FastAPI(
    title="DaiMinh AI Video Studio API",
    description="Professional AI-powered video editing backend",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "DaiMinh API"}

@app.get("/")
async def root():
    return {
        "service": "DaiMinh AI Video Studio Backend",
        "version": "1.0.0",
        "endpoints": {
            "auth": "/api/auth",
            "videos": "/api/videos",
            "projects": "/api/projects",
            "docs": "/docs"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
