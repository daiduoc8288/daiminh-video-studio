from fastapi import APIRouter, HTTPException
from app.schemas.project import ProjectResponse, ProjectCreate, ProjectUpdate
from typing import List

router = APIRouter()

# Temporary project storage
projects_db = {}

@router.post("/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate):
    """Create new project"""
    project_id = len(projects_db) + 1
    projects_db[project_id] = {
        "id": project_id,
        "user_id": 1,
        "name": project.name,
        "description": project.description,
        "status": "draft"
    }
    return projects_db[project_id]

@router.get("/", response_model=List[ProjectResponse])
async def list_projects():
    """Get all user projects"""
    return list(projects_db.values())

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: int):
    """Get project details"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects_db[project_id]

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: int, update: ProjectUpdate):
    """Update project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    project = projects_db[project_id]
    if update.name:
        project["name"] = update.name
    if update.description:
        project["description"] = update.description
    if update.status:
        project["status"] = update.status
    
    return project

@router.delete("/{project_id}")
async def delete_project(project_id: int):
    """Delete project"""
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    del projects_db[project_id]
    return {"message": "Project deleted"}
