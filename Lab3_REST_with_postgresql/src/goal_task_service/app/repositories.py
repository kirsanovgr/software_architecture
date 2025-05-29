from sqlalchemy.orm import Session
from typing import Optional, List

from app.models import Goal, Task


class GoalRepository:
    def create(self, db: Session, goal: Goal) -> Goal:
        db.add(goal)
        db.commit()
        db.refresh(goal)
        return goal
    
    def get_by_id(self, db: Session, id: int) -> Optional[Goal]:
        return db.query(Goal).filter(Goal.id == id).first()
    
    def get_all_goals(self, db: Session) -> List[Goal]:
        return db.query(Goal).all()
    
    def get_by_title(self, db: Session, title: str) -> Optional[Goal]:
        return db.query(Goal).filter(Goal.title == title).first()
    
    def update(self, db: Session, id: int, update_data: dict) -> Optional[Goal]:
        goal = self.get_by_id(db, id)
        if not goal:
            return None
        
        for key, value in update_data.items():
            if hasattr(goal, key):
                setattr(goal, key, value)
        
        db.commit()
        db.refresh(goal)
        return goal
        
    def delete(self, db: Session, id: int) -> bool:
        goal = self.get_by_id(db, id)
        if not goal:
            return False
        
        db.delete(goal)
        db.commit()
        
        return True
    
    
class TaskRepository:
    def create(self, db: Session, task: Task) -> Task:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def get_by_id(self, db: Session, id: int) -> Optional[Task]:
        return db.query(Task).filter(Task.id == id).first()
    
    def get_all_tasks(self, db: Session) -> List[Task]:
        return db.query(Task).all()

    def get_by_title(self, db: Session, title: str) -> Optional[Task]:
        return db.query(Task).filter(Task.title == title).first()

    def update(self, db: Session, id: int, update_data: dict) -> Optional[Task]:
        task = db.query(Task).filter(Task.id == id).first()
        if not task:
            return None
        for key, value in update_data.items():
            if hasattr(task, key):
                setattr(task, key, value)
        db.commit()
        db.refresh(task)
        return task

    def delete(self, db: Session, id: int) -> bool:
        task = db.query(Task).filter(Task.id == id).first()
        if not task:
            return False
        db.delete(task)
        db.commit()
        return True
    