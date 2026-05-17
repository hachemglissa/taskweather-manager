from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt
import hashlib

from .database import SessionLocal
from .models import Task, User
from .weather import get_weather

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt

security = HTTPBearer()
router = APIRouter()

# ================= DB =================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ================= DTO =================
class TaskRequest(BaseModel):
    title: str
    city: str

class UserRequest(BaseModel):
    username: str
    password: str

    # validation simple
    @classmethod
    def validate(cls, v):
        if not v.username or not v.password:
            raise ValueError("fields required")
        return v

# ================= JWT =================
SECRET_KEY = "d2603c6572d6d305b46ff02dbf1c3469"
ALGORITHM = "HS256"

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        return username

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def create_token(data: dict):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + timedelta(hours=2)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ================= PASSWORD (SHA256) =================
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain, hashed):
    return hashlib.sha256(plain.encode()).hexdigest() == hashed

# ================= AUTH =================

@router.post("/register")
def register(user: UserRequest, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()

    return {"message": "user created"}

@router.post("/login")
def login(user: UserRequest, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid username")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_token({"sub": user.username})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

# ================= TASKS =================

@router.post("/tasks")
def create_task(
    task: TaskRequest,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):

    weather = get_weather(task.city)

    new_task = Task(
        title=task.title,
        weather=f"{weather['condition']} {weather['temp']}°C"
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@router.get("/tasks")
def get_tasks(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):
    return db.query(Task).all()


@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)
):

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        return {"message": "Task not found"}

    db.delete(task)
    db.commit()

    return {"message": "deleted"}