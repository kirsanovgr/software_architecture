from sqlalchemy.orm import Session
from typing import Optional, List, Dict
from bson import ObjectId

from app.models import Goal, Task
from app.database_mongo import image_collection, text_collection, office_collection


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
    
    def save_file_info(self, db: Session, task_id: int, filename: str, mongo_id: str) -> Optional[Task]:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return None
        files = task.files or {}
        print(files)
        files[filename] = mongo_id
        print(files)
        task.files = dict(files)
        print(task.files)
        db.commit()
        db.refresh(task)
        
        fresh_task = db.query(Task).filter(Task.id == task_id).first()
        print("ACTUAL FROM DB:", fresh_task.files)
        
        return task

    def delete_file_info(self, db: Session, task_id: int, filename: str) -> Optional[Task]:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task or not task.files or filename not in task.files:
            return None
        del task.files[filename]
        db.commit()
        db.refresh(task)
        return task

    def get_all_files(self, db: Session, task_id: int) -> Optional[Dict[str, str]]:
        task = db.query(Task).filter(Task.id == task_id).first()
        return task.files if task else None

    def get_mongo_id(self, db: Session, task_id: int, filename: str) -> Optional[str]:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task or not task.files:
            return None
        return task.files.get(filename)


class FileRepository:
    def save_image(self, image_data: bytes) -> str:
        document = {"data": image_data}
        result = image_collection.insert_one(document)
        return str(result.inserted_id)

    def save_text(self, text_data: str, filename: str = None) -> str:
        document = {"text": text_data}
        if filename:
            document["filename"] = filename
        result = text_collection.insert_one(document)
        return str(result.inserted_id)

    def save_office_file(self, file_data: bytes, filename: str) -> str:
        document = {
            "filename": filename,
            "data": file_data
        }
        result = office_collection.insert_one(document)
        return str(result.inserted_id)

    def get_file_by_id(self, collection, file_id: str):
        return collection.find_one({"_id": ObjectId(file_id)})
    
    def delete_file_by_id(self, collection, file_id: str) -> bool:
        result = collection.delete_one({"_id": ObjectId(file_id)})
        return result.deleted_count > 0
    
    def delete_file_by_filename(self, collection, filename: str) -> bool:
        result = collection.delete_one({"filename": filename})
        return result.deleted_count > 0
