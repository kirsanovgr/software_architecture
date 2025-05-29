from fastapi import Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.repositories import UserRepository
from app.models import UserEntity
from app.schemas import UserEntityCreate, UserEntityRead, UserLogin, TakeToken
from app.auth import get_password_hash, verify_password, create_access_token, decode_access_token

class PasswordService:
    def create_hash(self, password: str) -> str:
        return get_password_hash(password=password)
    
    def check_pass(self, password: str, hashed: str) -> bool:
        return verify_password(password, hashed)
    
    def generate_token(self, data: dict) -> str:
        return create_access_token(data)
    
    def decode_token(self, token: str):
        return decode_access_token(token)

PASS_SERVICE = PasswordService()

class UserService:
    def __init__(self):
        self.repository = UserRepository()
        self.pass_service = PASS_SERVICE
        
    def create_user(self, db: Session, user_data: UserEntityCreate) -> UserEntity:
        user_data.password = self.pass_service.create_hash(user_data.password)
        new_user = UserEntity(**user_data.model_dump())
        return self.repository.create(db, new_user)
        
    def get_user_by_id(self, db: Session, id: int) -> Optional[UserEntityRead]:
        user = self.repository.get_user_by_id(db, id)
        if user is None:
            return None
        return UserEntityRead.model_validate(user)
        
    def get_user_by_nick(self, db: Session, nick: str) -> Optional[UserEntityRead]:
        user = self.repository.get_user_by_nick(db, nick)
        if user is None:
            return None
        return UserEntityRead.model_validate(user)
    
    def get_user_by_mask(self, db: Session, mask: str) -> Optional[UserEntity]:
        user = self.repository.get_users_by_mask(db, mask)
        if user is None:
            return None
        return UserEntityRead.model_validate(user)
    
    def update_user(self, db: Session, id: int, update_data: dict) -> Optional[UserEntityRead]:
        user = self.repository.get_user_by_id(db, id)
        if user is None:
            return None
        upd_user = self.repository.update(db, id, update_data)
        if upd_user is None:
            return None
        return UserEntityRead.model_validate(upd_user)
    
    def delete_user(self, db: Session, id: int):
        return self.repository.delete(db, id)
        
    def post_token(self, db: Session, user: UserLogin) -> TakeToken:
        nick = user.nick
        db_user = self.repository.get_user_by_nick(db, nick)
        
        if db_user is None:
            return None
        
        # try
        print(self.pass_service.check_pass(user.password, db_user.password))
        if self.pass_service.check_pass(user.password, db_user.password):
            token = self.pass_service.generate_token({
                "id": db_user.id,
                "nick": db_user.nick
            })
            
            if token:
                return TakeToken(access_token=token, token_type='bearer')
        
        return None
    
    def decode(self, token: str) -> TakeToken:
        return self.pass_service.decode_token(token)
    