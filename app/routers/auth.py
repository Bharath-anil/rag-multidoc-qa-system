from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"username": user.username, "user_id": user.id,}


@router.post("/register")
def register(data: LoginRequest, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == data.username).first()

    if existing:
        raise HTTPException(status_code=400, detail="User exists")

    user = User(username=data.username, password=data.password)
    db.add(user)
    db.commit()

    return {"message": "User created"}