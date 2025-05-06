from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from jose.exceptions import ExpiredSignatureError
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..auth import verify_password, create_access_token, ALGORITHM, SECRET_KEY, create_refresh_token
from ..crud import user as user_crud
from ..database import SessionLocal
from ..models.user import User
from ..schemas.user import UserResponse, UserCreate


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(tags=["auth"])


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username, "user_id": user.id, "role": user.role})
    new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(
        key="refresh_token",
        value=new_refresh_token,
        httponly=True,
        max_age=7 * 24 * 60 * 60,  # 7 days
        secure=False,  # set to True in production
        samesite="lax"
    )
    return response


@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    return user_crud.create_user(db, user_data)


@router.post("/auth/refresh-token")
def refresh_token(request: Request):
    request_refresh_token = request.cookies.get("refresh_token")
    if not request_refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = jwt.decode(request_refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=403, detail="Invalid refresh token")

        # Optional: Verify refresh token against DB
        new_token = create_access_token({"sub": user_id}, expires_delta=timedelta(minutes=15))
        return {"access_token": new_token}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid refresh token")
