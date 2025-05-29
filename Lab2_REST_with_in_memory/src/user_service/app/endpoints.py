from fastapi import APIRouter, Depends, HTTPException
from app.schemas import PostUser, GetUser, TakeToken, UserLogin
from app.services import UserService

router = APIRouter()

@router.post('/', response_model=GetUser)
def create_new_user(new_user: PostUser, service: UserService = Depends()) -> GetUser:
    return service.create_new_user(new_user)

@router.get('/all', response_model=list[GetUser])
def get_user_list(service: UserService = Depends()) -> list[GetUser]:
    users = service.get_all_users()
    if users:
        return users
    raise HTTPException(status_code=404, detail='No one user')

@router.get('/{id}', response_model=GetUser)
def get_user_by_id(id: int, service: UserService = Depends()) -> GetUser:
    usr = service.get_user_by_id(id)
    if usr:
        return usr
    raise HTTPException(status_code=404, detail=f'User by id={id} not found!')

@router.get('/search/{mask}', response_model=GetUser)
def search_user_using_mask(mask: str, service: UserService = Depends()) -> GetUser:
    usr = service.get_user_by_mask(mask)
    if usr:
        return usr
    raise HTTPException(status_code=404, detail=f'User by mask={mask} not found!')

@router.post('/token', response_model=TakeToken)
def generate_token(user: UserLogin, service: UserService = Depends()) -> TakeToken:
    token = service.post_token(user)
    if token:
        return token
    return HTTPException(status_code=400, detail=f'Invalid cerdentials!')

@router.get('/token/{token}')
def generate_token(token: str, service: UserService = Depends()):
    token = service.decode(token)
    if token:
        return token
    return HTTPException(status_code=400, detail=f'Invalid cerdentials!')