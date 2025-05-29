from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from app.endpoints import router
from app.services import UserService, PASS_SERVICE
from app.schemas import UserEntityCreate

import os

ADMIN_NICK = os.getenv("ADMIN_NICK", 'admin')
ADMIN_FIRST_NAME = os.getenv("ADMIN_FIRST_NAME", 'Admin')
ADMIN_SECOND_NAME = os.getenv("ADMIN_SECOND_NAME", 'Root')
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "1234")


@asynccontextmanager
async def lifespan(app: FastAPI):
    from app.database import SessionLocal, engine, Base
    
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        user_service = UserService()
        admin_exists = True if user_service.get_user_by_nick(db, ADMIN_NICK) else False
        
        print(ADMIN_PASSWORD)
        
        if not admin_exists:
            user_service.create_user(db, UserEntityCreate(
                nick=ADMIN_NICK,
                fname=ADMIN_FIRST_NAME,
                lname=ADMIN_SECOND_NAME,
                role='admin',
                password=ADMIN_PASSWORD
            ))
            print("Master user 'admin' created successfully")
    finally:
        db.close()

    yield

app = FastAPI(title="UserService", lifespan=lifespan)
app.include_router(router)

@app.get('/')
def get_root():
    return {"message": f"hello, from {app.title}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
