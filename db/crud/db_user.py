from datetime import timedelta

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from auth.auth_handler import get_password_hash, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from db.models.user import User
from sqlalchemy.orm.session import Session

from db.session import get_db
from schemas.user import UserCreate


def create_user(user: UserCreate, db: Session):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system",
        )
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        password=hashed_password,
        user_role="user",
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def admin_login(form_data: UserCreate, db):
    user = db.query(User).filter(User.email == form_data.email).first()
    if user is None or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"user": user.email}, expires_delta=access_token_expires)
    return {"id": user.id, "email": user.email, "access_token": access_token, "token_type": "bearer"}


def get_user_list(db):
    users = db.query(User).all()
    return users
