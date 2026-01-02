from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.schema import SessionLocal, User
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_user(payload: dict, db: Session = Depends(get_db)):
    # ⚠️ Para arrancar rápido uso dict; luego lo cambiamos a Pydantic schema
    required = ["username", "email", "full_name", "hashed_password"]
    missing = [k for k in required if k not in payload]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing fields: {', '.join(missing)}",
        )

    service = UserService(db)

    if service.get_user_by_username(payload["username"]):
        raise HTTPException(status_code=409, detail="Username already exists")

    if service.get_user_by_email(payload["email"]):
        raise HTTPException(status_code=409, detail="Email already exists")

    user = service.create_user(
        username=payload["username"],
        email=payload["email"],
        full_name=payload["full_name"],
        hashed_password=payload["hashed_password"],
    )

    # No devolver hashed_password
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
    }


@router.get("/{username}", response_model=dict)
def get_user(username: str, db: Session = Depends(get_db)):
    service = UserService(db)
    user = service.get_user_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
    }
