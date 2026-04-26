from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.user import User
from pydantic import BaseModel
from app.core.auth import (
    hash_password,
    verify_password,
    create_access_token
)
router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/register")
def register(data: LoginRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()

    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    user = User(
        username=data.username,
        hashed_password=hash_password(data.password) 
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created"}