from pydantic import BaseModel, Field

class UserRegisterRequest(BaseModel):
    phone_number: str = Field(..., pattern=r"^0\d{9}$")
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=6)

class UserLoginRequest(BaseModel):
    phone_number: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str = "CUSTOMER"
