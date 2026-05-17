from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import Task
from .weather import get_weather

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tasks")
def create_task(title: str, city: str, db: Session = Depends(get_db)):

    weather = get_weather(city)

    task = Task(
        title=title,
        weather=f"{weather['condition']} {weather['temp']}°C"
    )

    db.add(task)
    db.commit()
    db.refresh(task)

    return task


@router.get("/tasks")
def get_tasks(db: Session = Depends(get_db)):
    return db.query(Task).all()


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    db.delete(task)
    db.commit()
    return {"message": "deleted"}