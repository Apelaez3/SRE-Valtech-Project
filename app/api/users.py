from fastapi import APIRouter, HTTPException, Depends

from app.db.schema  import SessionLocal
from app.models.user import UserCreate, UserRead 
from app.services.user_service import UserService

router = APIRouter()

def get_user_service() -> UserService: 
    return UserService(session = SessionLocal())

@router.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    db_user = user_service.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(user=user)