from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas import GoalCreate, GoalRead, TaskCreate, TaskRead
from app.repositories import GoalRepository, TaskRepository
from app.models import Goal, Task

class GoalService:
    def __init__(self):
        self.repository = GoalRepository()
        
    def get_all_goals(self, db: Session) -> List[Goal]:
        return self.repository.get_all_goals(db)

    def create_goal(self, db: Session, goal_data: GoalCreate, owner: str) -> Goal:
        goal_data.owner_nick = owner
        goal = Goal(**goal_data.model_dump())
        return self.repository.create(db, goal)

    def get_goal_by_id(self, db: Session, goal_id: int) -> Optional[GoalRead]:
        goal = self.repository.get_by_id(db, goal_id)
        if goal is None:
            return None
        return GoalRead.model_validate(goal)

    def get_goal_by_title(self, db: Session, title: str) -> Optional[GoalRead]:
        goal = self.repository.get_by_title(db, title)
        if goal is None:
            return None
        return GoalRead.model_validate(goal)

    def update_goal(self, db: Session, goal_id: int, update_data: dict, owner: str) -> Optional[GoalRead]:
        goal = self.repository.get_by_id(db, goal_id)
        if goal.owner_nick != owner:
            return None
        if goal is None:
            return None
        new_goal = self.repository.update(db, goal_id, update_data)
        if new_goal is None:
            return False
        return GoalRead.model_validate(new_goal)

    def delete_goal(self, db: Session, goal_id: int, owner: str) -> bool:
        goal = self.repository.get_by_id(db, goal_id)
        if goal.owner_nick == owner:
            return self.repository.delete(db, goal_id)
        return False
    
    
class TaskService:
    def __init__(self):
        self.repository = TaskRepository()
        
    def get_all_task(self, db: Session) -> List[Task]:
        return self.repository.get_all_tasks(db)

    def create_task(self, db: Session, task_data: TaskCreate, owner: str) -> TaskRead:
        task_data.owner_nick = owner
        task = Task(**task_data.model_dump())
        created_task = self.repository.create(db, task)
        return TaskRead.model_validate(created_task)

    def get_task_by_id(self, db: Session, task_id: int) -> Optional[TaskRead]:
        task = self.repository.get_by_id(db, task_id)
        if task is None:
            return None
        return TaskRead.model_validate(task)

    def get_task_by_title(self, db: Session, title: str) -> Optional[TaskRead]:
        task = self.repository.get_by_title(db, title)
        if task is None:
            return None
        return TaskRead.model_validate(task)

    def update_task(self, db: Session, task_id: int, update_data: dict, owner: str) -> Optional[TaskRead]:
        cur_task = self.repository.get_by_id(db, task_id)
        if cur_task.owner_nick != owner:
            return None
        task = self.repository.update(db, task_id, update_data)
        if task is None:
            return None
        return TaskRead.model_validate(task)
        

    def delete_task(self, db: Session, task_id: int, owner: str) -> bool:
        cur_task = self.repository.get_by_id(db, task_id)
        if cur_task.owner_nick == owner:
            return self.repository.delete(db, task_id)
        return False