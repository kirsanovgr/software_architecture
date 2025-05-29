from sqlalchemy.orm import Session
from typing import Optional, List

from app.schemas import GoalCreate, GoalRead, TaskCreate, TaskRead
from app.repositories import GoalRepository, TaskRepository, FileRepository
from app.models import Goal, Task
from app.repositories import (
    image_collection,
    text_collection,
    office_collection,
)

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
        self.file_repository = FileRepository()
        
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
        
    def add_file(self, db: Session, task_id: int, file_data: bytes, filename: str, file_type: str) -> Optional[Task]:
        if file_type == "image":
            mongo_id = self.file_repository.save_image(file_data)
        elif file_type == "text":
            mongo_id = self.file_repository.save_text(file_data.decode("utf-8"), filename)
        else:
            mongo_id = self.file_repository.save_office_file(file_data, filename)

        print(task_id, filename, mongo_id)
        return self.repository.save_file_info(db, task_id, filename, mongo_id)

    def del_file_by_name(self, db: Session, task_id: int, file_name: str) -> Optional[Task]:
        task = self.repository.get_by_id(db, task_id)
        if not task or not task.files or file_name not in task.files:
            return None

        mongo_id = task.files[file_name]
        deleted = False

        # Удалить из всех коллекций
        for collection in [image_collection, text_collection, office_collection]:
            if self.file_repository.delete_file_by_id(collection, mongo_id):
                deleted = True
                break

        if deleted:
            return self.repository.delete_file_info(db, task_id, file_name)
        return None

    def del_file_by_id(self, db: Session, task_id: int, file_id: str) -> Optional[Task]:
        task = self.repository.get_by_id(db, task_id)
        if not task or not task.files:
            return None

        # Найти файл по MongoID
        file_name = next((name for name, fid in task.files.items() if fid == file_id), None)
        if file_name is None:
            return None

        return self.del_file_by_name(db, task_id, file_name)
        
    def delete_task(self, db: Session, task_id: int, owner: str) -> bool:
        task = self.repository.get_by_id(db, task_id)
        if not task or task.owner_nick != owner:
            return False
            
        if task.files:
            for mongo_id in task.files.values():
                for collection in [image_collection, text_collection, office_collection]:
                    self.file_repository.delete_file_by_id(collection, mongo_id)
    
        return self.repository.delete(db, task_id)