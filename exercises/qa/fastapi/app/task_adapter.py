"""
The TaskAdapter class is responsible for making calls to the database.

Using this adapter facilitates testing by allowing us to mock the database calls without reimplementing
the interface to the sqlalchemy class.

The adapter is tested by integration tests, to make sure it works with the database correctly.
"""
from sqlalchemy.orm import Session
from . import models, schemas


class TaskAdapter:

  def __init__(self, db=Session):
    self.db = db

  def get_task(self, task_id: int):
      return self.db.query(models.Task).filter(models.Task.id == task_id).first()

  def get_tasks(self, skip: int = 0, limit: int = 10):
    return self.db.query(models.Task).offset(skip).limit(limit).all()

  def create_task(self, task: schemas.TaskCreate):
      db_task = models.Task(
          title=task.title, description=task.description, completed=task.completed
      )
      self.db.add(db_task)
      self.db.commit()
      self.db.refresh(db_task)
      return db_task

  def update_task(self, task: schemas.TaskCreate, task_id: int):
      db_task = self.get_task(task_id)
      if db_task:
          db_task.title = task.title
          db_task.description = task.description
          db_task.completed = task.completed
          self.db.commit()
          self.db.refresh(db_task)
          return db_task

  def delete_task(self, task_id: int):
      db_task = self.get_task(task_id)
      if db_task:
          self.db.delete(db_task)
          self.db.commit()
          return db_task
