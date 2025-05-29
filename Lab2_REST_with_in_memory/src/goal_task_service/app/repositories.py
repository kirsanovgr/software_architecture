from app.database_memory import TASK_LIST, GOAL_LIST
from app.schemas import PostGoal, GetGoal, GetTask, PostTask
from app.models import GoalEntity, TaskEntity

class GoalRepository:
    def add_goal(self, new_goal: PostGoal, owner_nick: str) -> GetGoal:
        tmp_goal = GoalEntity(
            title=new_goal.title,
            description=new_goal.description,
            owner_nick=owner_nick,
        )
        GOAL_LIST.append(tmp_goal)
        return GetGoal(
            id=tmp_goal.id,
            title=tmp_goal.title,
            description=tmp_goal.description,
            owner_nick=tmp_goal.owner_nick,
            created_at=tmp_goal.created_at
        )
        
    def get_all_goals(self) -> list[GetGoal]:
        tmp = []
        for tmp_goal in GOAL_LIST:
            tmp.append(
                GetGoal(
                    id=tmp_goal.id,
                    title=tmp_goal.title,
                    description=tmp_goal.description,
                    owner_nick=tmp_goal.owner_nick,
                    created_at=tmp_goal.created_at
                )
            )
        return tmp
    
    def get_all_owner_goals(self, owner_nick: str) -> list[GetGoal]:
        tmp = self.get_all_goals()
        ans = []
        for goal in tmp:
            if goal.owner_nick == owner_nick:
                ans.append(goal)
        return ans
    

class TaskRepository:
    def add_task(self, new_goal: PostTask, owner_nick: str) -> GetTask:
        tmp_task = TaskEntity(
            title=new_goal.title,
            description=new_goal.description,
            owner_nick=owner_nick,
        )
        TASK_LIST.append(tmp_task)
        return GetTask(
            id=tmp_task.id,
            title=tmp_task.title,
            description=tmp_task.description,
            owner_nick=tmp_task.owner_nick,
            created_at=tmp_task.created_at,
            status=tmp_task.status,
            files=tmp_task.files
        )
        
    def get_all_tasks(self) -> list[GetTask]:
        tmp = []
        for tmp_task in TASK_LIST:
            tmp.append(
                GetTask(
                    id=tmp_task.id,
                    title=tmp_task.title,
                    description=tmp_task.description,
                    owner_nick=tmp_task.owner_nick,
                    created_at=tmp_task.created_at,
                    status=tmp_task.status,
                    files=tmp_task.files
                )
            )
        return tmp
    
    def get_all_owner_tasks(self, owner_nick: str) -> list[GetTask]:
        tmp = self.get_all_tasks()
        ans = []
        for task in tmp:
            if task.owner_nick == owner_nick:
                ans.append(task)
        return ans
    
    def get_all_owner_tasks_with_status(self, owner_nick: str, status: str) -> list[GetTask]:
        tmp = self.get_all_owner_tasks(owner_nick)
        ans = []
        for task in tmp:
            if task.status == status:
                ans.append(task)
        return ans