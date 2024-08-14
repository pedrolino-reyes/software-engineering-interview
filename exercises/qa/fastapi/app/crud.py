from sqlalchemy.orm import Session
from . import models, schemas
from fastapi import HTTPException


def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate):
    # Title length validation
    if len(task.title) < 5 or len(task.title) > 50:
        raise HTTPException(
            status_code=400, detail="Title length must be between 5 and 50 characters"
        )

    # Description length validation
    if len(task.description) < 10:
        raise HTTPException(
            status_code=400, detail="Description length must be at least 10 characters"
        )

    db_task = models.Task(
        title=task.title, description=task.description, completed=task.completed
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task: schemas.TaskCreate, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db_task.title = task.title
        db_task.description = task.description
        db_task.completed = task.completed
        db.commit()
        db.refresh(db_task)
        return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if db_task:
        db.delete(db_task)
        db.commit()
        return db_task
