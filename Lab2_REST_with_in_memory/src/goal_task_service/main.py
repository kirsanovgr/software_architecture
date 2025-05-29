# Илья Сергеевич, не ругайтесь, питон это хорошо, когда надо рвать себя и срочно за меньше чем неделю все делать...

from fastapi import FastAPI
from app.endpoints import grouter, trouter

app = FastAPI(title="GoalTaskService")
app.include_router(grouter, prefix="/goals")
app.include_router(trouter, prefix="/tasks")

@app.get('/')
def get_root():
    return {"message": f"hello, from {app.title}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)