from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app import models, schemas
from app.security import get_password_hash, verify_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/register", response_model=schemas.UserRead, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # 0) Normalize and truncate password so bcrypt is always happy
        raw_password = user_in.password or ""
        if len(raw_password) > 72:
            raw_password = raw_password[:72]

        # 1) Check if email already exists
        existing = db.query(models.User).filter(models.User.email == user_in.email).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        # 2) Hash the (possibly truncated) password
        hashed_pw = get_password_hash(raw_password)

        # 3) Create user in DB
        user = models.User(
            email=user_in.email,
            hashed_password=hashed_pw,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except HTTPException:
        raise
    except Exception as e:
        # Debug detail, so we see real errors
        raise HTTPException(
            status_code=500,
            detail=f"Register error: {e!r}",
        )


class LoginRequest(schemas.UserBase):
    password: str


@router.post("/login")
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    try:
        raw_password = login_data.password or ""
        if len(raw_password) > 72:
            raw_password = raw_password[:72]

        # Find the user by email
        user = db.query(models.User).filter(models.User.email == login_data.email).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        # Check password
        if not verify_password(raw_password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

        return {
            "message": "Login successful",
            "user": {"id": user.id, "email": user.email},
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Login error: {e!r}",
        )
