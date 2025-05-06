from sqlalchemy.orm import Session
from ..models import user as model
from ..schemas import user as schema
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: schema.UserCreate):
    # db_user = model.User(**user.dict())
    hashed_password = get_password_hash(user.password)
    db_user = model.User(username=user.username, password=hashed_password, email=user.email, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(model.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(model.User).filter(model.User.id == user_id).first()
