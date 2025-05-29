from fastapi import Depends
from app.models import UserEntity
from app.schemas import GetUser, PostUser, UserLogin, TakeToken
from app.auth import get_password_hash, verify_password, create_access_token, decode_access_token
from app.repositories import UserRepository

class PasswordService:
    def create_hash(self, password: str) -> str:
        return get_password_hash(password=password)
    
    def check_pass(self, password: str, hash: str) -> bool:
        return verify_password(password, hash)
    
    def generate_token(self, data: dict) -> str:
        return create_access_token(data)
    
    def decode_token(self, token: str):
        return decode_access_token(token)
        
        

class UserService:
    
    def __init__(self, pass_service: PasswordService = Depends(), repo: UserRepository = Depends()):
        self.pass_service = pass_service
        self.repo = repo
    
    def create_new_user(self, new_user: PostUser) -> GetUser:
        usr = UserEntity(
            id = UserEntity.NEXTID,
            nick=new_user.nick,
            fname=new_user.fname,
            lname=new_user.lname,
            password_hash=self.pass_service.create_hash(new_user.password)
        )

        self.repo.create_user(usr)
        
        return GetUser(
            nick=usr.nick,
            fname=usr.fname,
            lname=usr.lname
        )
        
    def get_all_users(self) -> list[GetUser]:
        users = self.repo.get_all_users()
        get_usr_list = []
        for usr in users:
            get_usr_list.append(
                GetUser(
                    nick=usr.nick,
                    fname=usr.fname,
                    lname=usr.lname
                )
            )
        return get_usr_list
    
    def get_user_by_id(self, id: int) -> GetUser:
        users = self.repo.get_all_users()
        for usr in users:
            if usr.id == id:
                return GetUser(
                    nick=usr.nick,
                    fname=usr.fname,
                    lname=usr.lname
                )
        return None

    def get_user_by_mask(self, mask: str) -> GetUser:
        users = self.repo.get_all_users()
        mask = ''.join(mask.split(' ')).lower()
        for usr in users:
            explore = f'{usr.fname.lower()}{usr.lname.lower()}'
            if mask in explore:
                return GetUser(
                    nick=usr.nick,
                    fname=usr.fname,
                    lname=usr.lname
                )
        return None
    
    def post_token(self, user: UserLogin) -> TakeToken:
        users = self.repo.get_all_users()
        search_user = None
        for usr in users:
            if usr.nick == user.nick:
                search_user = usr
        
        if search_user:
            if self.pass_service.check_pass(user.password, search_user.password_hash):
                token = self.pass_service.generate_token({
                    "id": search_user.id,
                    "nick": search_user.nick
                })
                if token:
                    return TakeToken(access_token=token, token_type="bearer")
            
        return None
    
    def decode(self, token: str) -> TakeToken:
        return self.pass_service.decode_token(token)