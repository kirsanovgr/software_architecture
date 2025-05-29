from fastapi import Depends
from app.repositories import GoalRepository, TaskRepository
from app.schemas import PostGoal, GetGoal, GetTask, PostTask

class GoalService:
    
    def __init__(self, repo: GoalRepository = Depends()):
        self.repo = repo  # DI
    
    def add_goal(self, new_goal: PostGoal, owner_nick: str) -> GetGoal:
        tmp_goal = self.repo.add_goal(new_goal, owner_nick)
        if tmp_goal:
            return tmp_goal
        return None
    
    def get_all_goals(self) -> list[GetGoal]:
        tmp_goals = self.repo.get_all_goals()
        if tmp_goals:
            return tmp_goals
        return None
    
    def get_all_owner_goals(self, owner_nick: str) -> list[GetGoal]:
        tmp_goals = self.repo.get_all_owner_goals(owner_nick)
        if tmp_goals:
            return tmp_goals
        return None
    

class TaskService:
    
    def __init__(self, repo: TaskRepository = Depends()):
        self.repo = repo # DI
        
    def add_task(self, new_goal: PostTask, owner_nick: str) -> GetTask:
        tmp_task = self.repo.add_task(new_goal, owner_nick)
        if tmp_task:
            return tmp_task
        return None
    
    def get_all_tasks(self) -> list[GetTask]:
        tmp_task = self.repo.get_all_tasks()
        if tmp_task:
            return tmp_task
        return None
    
    def get_all_owner_tasks(self, owner_nick: str) -> list[GetTask]:
        tmp_task = self.repo.get_all_owner_tasks(owner_nick)
        if tmp_task:
            return tmp_task
        return None
    
    def get_all_owner_tasks_with_status(self, owner_nick: str, status: str) -> list[GetTask]:
        tmp_task = self.repo.get_all_owner_tasks_with_status(owner_nick, status)
        if tmp_task:
            return tmp_task
        return None
        
        
        