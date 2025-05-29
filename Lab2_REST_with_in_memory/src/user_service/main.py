# Илья Сергеевич, не ругайтесь, питон это хорошо, когда надо рвать себя и срочно за меньше чем неделю все делать...

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.endpoints import router
from app.services import UserService, PasswordService
from app.repositories import UserRepository
from app.schemas import PostUser

@asynccontextmanager
async def lifespan(app: FastAPI):
    service = UserService(
        pass_service=PasswordService(),
        repo=UserRepository()
    )

    users = service.repo.get_all_users()
    admin_exists = any(user.nick == "admin" for user in users)

    if not admin_exists:
        service.create_new_user(PostUser(
            nick="admin",
            fname="Admin",
            lname="User",
            password="secret"
        ))
        print("Master user 'admin' created successfully")

    yield

app = FastAPI(title="UserService", lifespan=lifespan)
app.include_router(router, prefix='/usr')

@app.get('/')
def get_root():
    return {"message": f"hello, from {app.title}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
