from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserRegisterRequest, UserLoginRequest, TokenResponse
from app.core.security import get_password_hash, verify_password, create_access_token
from app.repositories.user_repo import UserRepository

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(req: UserRegisterRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    existing = repo.get_by_phone(req.phone_number)
    if existing:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Số điện thoại đã được đăng ký.")
    hashed_pwd = get_password_hash(req.password)
    repo.create(phone=req.phone_number, full_name=req.full_name, password_hash=hashed_pwd, role="CUSTOMER")
    token = create_access_token(subject=req.phone_number, role="CUSTOMER")
    return TokenResponse(access_token=token, role="CUSTOMER")

@router.post("/login", response_model=TokenResponse)
def login(req: UserLoginRequest, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_phone(req.phone_number)
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sai số điện thoại hoặc mật khẩu.")
    token = create_access_token(subject=req.phone_number, role=user.role)
    return TokenResponse(access_token=token, role=user.role)
