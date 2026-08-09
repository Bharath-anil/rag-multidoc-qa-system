from pydantic import BaseModel,Field,field_validator


class LoginRequest(BaseModel):
    username: str
    password: str

    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "username",
                "password": "StrongPassword123"
            }
        }
    }


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class RegisterRequest(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    password: str = Field(min_length=8)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):
        value = value.strip()

        if " " in value:
            raise ValueError("Username cannot contain spaces")

        return value

class RegisterResponse(BaseModel):
    message: str