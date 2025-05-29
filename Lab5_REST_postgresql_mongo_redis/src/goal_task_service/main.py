from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.endpoints import goal_router, task_router
from app.services import GoalService, TaskService
from app.schemas import GoalCreate, TaskCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database import SessionLocal, engine, Base
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        goal_service = GoalService()
        task_service = TaskService()
        
        new_goal = GoalCreate(
            title="Купить пиво",
            text="Срочно купить много пиво",
            owner_nick="Димка корзинка"
        )
        
        if not goal_service.get_goal_by_title(db, new_goal.title):
            goal_service.create_goal(db, new_goal, owner="Димка корзинка")
            
        new_goal = GoalCreate(
            title="Купить слона",
            text="Срочно купить много слонов",
            owner_nick="Димка корзинка"
        )
        
        if not goal_service.get_goal_by_title(db, new_goal.title):
            goal_service.create_goal(db, new_goal, owner="Димка корзинка")
        
        new_task = TaskCreate(
            title="Купить пиво",
            text="Срочно купить много пиво",
            owner_nick="Димка корзинка",
            goal_id=1
        )
        if not task_service.get_task_by_title(db, new_task.title):
            task_service.create_task(db, new_task, owner="Димка корзинка")
        
    finally:
        db.close()
        
    yield

app = FastAPI(title="GoalTaskService", lifespan=lifespan)

app.include_router(goal_router)
app.include_router(task_router)

@app.get('/')
def get_root():
    return { "massage": f"hello from {app.title}" }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app="main:app", host="0.0.0.0", port=8001)