from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas import TakeToken, UserLogin, UserEntityRead, UserEntityCreate
from app.services import UserService
from app.database import get_db

router = APIRouter()
user_service = UserService()

@router.post('/user', response_model=UserEntityRead)
def create_new_user(new_user: UserEntityCreate, db: Session = Depends(get_db)) -> UserEntityRead:
    return user_service.create_user(db, new_user)

@router.get('/user/id-{id}', response_model=UserEntityRead)
def get_user_by_id(id: int, db: Session = Depends(get_db)) -> UserEntityRead:
    user = user_service.get_user_by_id(db, id)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User not found by id({id})")
    return user
    
@router.get('/user/nick-{nick}', response_model=UserEntityRead)
def get_user_by_nickname(nick: str, db: Session = Depends(get_db)) -> UserEntityRead:
    user = user_service.get_user_by_nick(db, nick)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User not found by nick({nick})")
    return user
    
@router.get('/user/m-{mask}', response_model=UserEntityRead)
def search_user_using_mask(mask: str, db: Session = Depends(get_db)) -> UserEntityRead:
    user = user_service.get_user_by_mask(db, mask)
    if user is None:
        raise HTTPException(status_code=404, detail=f"User not found by mak(%{mask}%)")
    return user

@router.delete('/user/id-{id}', response_model=bool)
def delete_user(id: int, db: Session = Depends(get_db)) -> bool:
    is_deleted = user_service.delete_user(db, id)
    if is_deleted:
        return is_deleted
    raise HTTPException(status_code=404, detail="User not found") 

@router.put('/user/id-{id}', response_model=UserEntityRead)
def update_user(id: int, update_data: dict, db: Session = Depends(get_db)) -> UserEntityRead:
    updated_user = user_service.update_user(db, id, update_data)
    if updated_user:
        return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@router.post('/token', response_model=TakeToken)
def generate_token(user: UserLogin, db: Session = Depends(get_db)) -> TakeToken:
    token = user_service.post_token(db, user)
    if token:
        return token
    raise HTTPException(status_code=400, detail='Invalid cerdentials!')

@router.get('/token')
def decode_token(token: str, db: Session = Depends(get_db)):
    token = user_service.decode(token)
    if token:
        return token
    raise HTTPException(status_code=400, detail=f'Invalid cerdentials!')