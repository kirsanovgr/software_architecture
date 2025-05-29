from datetime import datetime, timezone

class GoalEntity:
    
    NEXTID = 0
    
    def __init__(self, title: str, description: str, owner_nick: str, created_at: datetime = datetime.now(timezone.utc)):
        self.id = GoalEntity.NEXTID
        GoalEntity.NEXTID += 1
        self.title = title
        self.description = description
        self.owner_nick = owner_nick
        self.created_at = created_at
        

class TaskEntity:
    
    NEXTID = 0
    
    def __init__(self, title: str, description: str, owner_nick: str, created_at: datetime = datetime.now(timezone.utc),  status: str = 'CREATED'):
        self.id = TaskEntity.NEXTID
        TaskEntity.NEXTID += 1
        self.title = title
        self.description = description
        self.owner_nick = owner_nick
        self.created_at = created_at
        self.status = status
        self.files: list[str] = []
        