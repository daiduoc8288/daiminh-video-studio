from fastapi import APIRouter, HTTPException, status
from app.schemas.user import UserCreate, UserResponse, LoginRequest, Token
from datetime import timedelta

router = APIRouter()

# Temporary in-memory user storage (replace with DB)
users_db = {}

@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    """User registration endpoint"""
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Store user (in production, hash password!)
    users_db[user.email] = {
        "id": len(users_db) + 1,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "is_active": True
    }
    
    return users_db[user.email]

@router.post("/login", response_model=Token)
async def login(credentials: LoginRequest):
    """User login endpoint"""
    user = users_db.get(credentials.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # In production: verify hashed password
    return {
        "access_token": f"token-{user['id']}",
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user():
    """Get current user info"""
    # In production: validate token
    return {"id": 1, "email": "user@example.com", "username": "user", "full_name": "Test User", "is_active": True}
