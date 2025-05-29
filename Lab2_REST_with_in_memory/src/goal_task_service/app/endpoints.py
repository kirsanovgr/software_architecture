from fastapi import APIRouter, Depends, HTTPException
from app.schemas import GetGoal, PostGoal, GetTask, PostTask
from app.services import GoalService, TaskService
from app.auth import get_current_user

grouter = APIRouter()

@grouter.post("/", response_model=GetGoal)
def add_new_goal(new_goal: PostGoal, service: GoalService = Depends(), nickname: str = Depends(get_current_user)) -> GetGoal:
    response = service.add_goal(new_goal, nickname)
    if response:
        return response
    return HTTPException(status_code=401, detail="Some error")

@grouter.get("/all", response_model=list[GetGoal])
def get_all_goals(service: GoalService = Depends()) -> list[GetGoal]:
    response = service.get_all_goals()
    if response:
        return response
    return HTTPException(status_code=404, detail="No one goals")

@grouter.get("/user", response_model=list[GetGoal])
def get_all_goals(service: GoalService = Depends(), nickname: str = Depends(get_current_user)) -> list[GetGoal]:
    response = service.get_all_owner_goals(nickname)
    if response:
        return response
    return HTTPException(status_code=404, detail=f"No one goals of user {nickname}")


trouter = APIRouter()

@trouter.post("/", response_model=GetTask)
def add_new_task(new_task: PostTask, service: TaskService = Depends(), nickname: str = Depends(get_current_user)) -> GetTask:
    response = service.add_task(new_task, nickname)
    if response:
        return response
    return HTTPException(status_code=401, detail="Some error")

@trouter.get("/all", response_model=list[GetTask])
def get_all_tasks(service: TaskService = Depends()) -> list[GetTask]:
    response = service.get_all_tasks()
    if response:
        return response
    return HTTPException(status_code=404, detail="No one goals")

@trouter.get("/user", response_model=list[GetTask])
def get_all_goals(service: TaskService = Depends(), nickname: str = Depends(get_current_user)) -> list[GetTask]:
    response = service.get_all_owner_tasks(nickname)
    if response:
        return response
    return HTTPException(status_code=404, detail=f"No one goals of user {nickname}")

@trouter.get("/user/{status}", response_model=list[GetTask])
def get_all_goals(status: str, service: TaskService = Depends(), nickname: str = Depends(get_current_user)) -> list[GetTask]:
    response = service.get_all_owner_tasks_with_status(nickname, status)
    if response:
        return response
    return HTTPException(status_code=404, detail=f"No one goals of user {nickname}")