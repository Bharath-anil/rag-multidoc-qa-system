from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "user name",
                "password": "StrongPassword123"
            }
        }
    }


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class RegisterResponse(BaseModel):
    message: str