from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List

from app.schemas import TaskCreate, TaskRead, GoalCreate, GoalRead
from app.services import TaskService, GoalService
from app.database import get_db
from app.auth import get_current_user

goal_router = APIRouter()
goal_service = GoalService()
task_router = APIRouter()
task_service = TaskService()

# Создание задачи
@task_router.post("/tasks/", response_model=TaskRead)
def create_task(task: TaskCreate, db: Session = Depends(get_db), nick: str = Depends(get_current_user)):
    return task_service.create_task(db, task, nick)

@task_router.get("/tasks/all", response_model=List[TaskRead])
def get_all_tasks(db: Session = Depends(get_db)):
    return [TaskRead.model_validate(el) for el in task_service.get_all_task(db)]

# Получение задачи по ID
@task_router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task_by_id(task_id: int, db: Session = Depends(get_db)):
    task = task_service.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

# Получение задач по заголовку
@task_router.get("/tasks/", response_model=TaskRead)
def get_tasks_by_title(title: str, db: Session = Depends(get_db)):
    tasks = task_service.get_task_by_title(db, title)
    if not tasks:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return tasks

# Обновление задачи
@task_router.put("/tasks/{task_id}", response_model=TaskRead)
def update_task(task_id: int, update_data: dict, db: Session = Depends(get_db), nick: str = Depends(get_current_user)):
    updated_task = task_service.update_task(db, task_id, update_data, nick)
    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return updated_task

# Удаление задачи
@task_router.delete("/tasks/{task_id}", response_model=bool)
def delete_task(task_id: int, db: Session = Depends(get_db), nick: str = Depends(get_current_user)):
    is_deleted = task_service.delete_task(db, task_id, nick)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Task not found")
    return is_deleted

@task_router.post("/tasks/{task_id}/upload", response_model=TaskRead)
def upload_file_to_task(
    task_id: int,
    file: UploadFile = File(...),
    file_type: str = Form(...),  # 'image', 'text', 'office'
    db: Session = Depends(get_db)
):
    contents = file.file.read()
    updated_task = task_service.add_file(
        db=db,
        task_id=task_id,
        file_data=contents,
        filename=file.filename,
        file_type=file_type
    )
    if not updated_task:
        raise HTTPException(status_code=404, detail="Failed to upload file")
    return TaskRead.model_validate(updated_task)


@task_router.delete("/tasks/{task_id}/file-by-name", response_model=TaskRead)
def delete_file_by_name(
    task_id: int,
    file_name: str,
    db: Session = Depends(get_db)
):
    updated_task = task_service.del_file_by_name(db, task_id, file_name)
    if not updated_task:
        raise HTTPException(status_code=404, detail="File not found in task")
    return TaskRead.model_validate(updated_task)


@task_router.delete("/tasks/{task_id}/file-by-id", response_model=TaskRead)
def delete_file_by_id(
    task_id: int,
    file_id: str,
    db: Session = Depends(get_db)
):
    updated_task = task_service.del_file_by_id(db, task_id, file_id)
    if not updated_task:
        raise HTTPException(status_code=404, detail="File not found in task")
    return TaskRead.model_validate(updated_task)





@goal_router.post("/goals/", response_model=GoalRead)
def create_goal(goal: GoalCreate, db: Session = Depends(get_db), nick: str = Depends(get_current_user)):
    return goal_service.create_goal(db, goal, nick)

@goal_router.get("/goals/all", response_model=List[GoalRead])
def get_all_goals(db: Session = Depends(get_db)):
    return [GoalRead.model_validate(el) for el in goal_service.get_all_goals(db)]

# Получение цели по ID
@goal_router.get("/goals/{goal_id}", response_model=GoalRead)
def get_goal_by_id(goal_id: int, db: Session = Depends(get_db)):
    goal = goal_service.get_goal_by_id(db, goal_id)
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

# Получение цели по заголовку
@goal_router.get("/goals/", response_model=GoalRead)
def get_goals_by_title(title: str, db: Session = Depends(get_db)):
    goals = goal_service.get_goal_by_title(db, title)
    if not goals:
        raise HTTPException(status_code=404, detail="Goals not found")
    return goals

# Обновление цели
@goal_router.put("/goals/{goal_id}", response_model=GoalRead)
def update_goal(goal_id: int, update_data: dict, db: Session = Depends(get_db), nick: str = Depends(get_current_user)):
    updated_goal = goal_service.update_goal(db, goal_id, update_data, nick)
    if not updated_goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return updated_goal

# Удаление цели
@goal_router.delete("/goals/{goal_id}", response_model=bool)
def delete_goal(goal_id: int, db: Session = Depends(get_db), nick: str = Depends(get_current_user)):
    is_deleted = goal_service.delete_goal(db, goal_id, nick)
    if not is_deleted:
        raise HTTPException(status_code=404, detail="Goal not found")
    return is_deleted