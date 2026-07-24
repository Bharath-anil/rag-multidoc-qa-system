from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.dependencies import get_db
from app.models.user import User
from pydantic import BaseModel
from app.core.auth import (  hash_password, verify_password, create_access_token)
from app.schemas.auth import ( LoginRequest, LoginResponse,  RegisterResponse)
router = APIRouter(prefix="/auth",  tags=["Authentication"],)

@router.post("/login",
                response_model=LoginResponse,
                summary="Authenticate user",
                description="Authenticates a registered user and returns a JWT access token.",
                response_description="JWT access token generated successfully.",
                responses={
                401: {"description": "Invalid username or password."}
                },)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"user_id": user.id})

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/register",
             response_model=RegisterResponse, 
             status_code=201,
             summary="Register new user",
             description="Creates a new user account with a securely hashed password.",
             response_description="User account created successfully.",
             responses={
                 400: {"description": "Username already exists."}
             },)
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