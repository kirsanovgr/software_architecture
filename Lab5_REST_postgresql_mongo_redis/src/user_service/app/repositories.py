from sqlalchemy import or_
from sqlalchemy.orm import Session
from typing import Optional, List

from app.models import UserEntity

class UserRepository:
    def create(self, db: Session, user: UserEntity) -> UserEntity:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    def get_user_by_id(self, db: Session, id: int) -> Optional[UserEntity]:
        return db.query(UserEntity).filter(UserEntity.id == id).first()
    
    def get_user_by_nick(self, db: Session, nick: str) -> Optional[UserEntity]:
        return db.query(UserEntity).filter(UserEntity.nick == nick).first()

    def get_users_by_mask(self, db: Session, pattern: str) -> List[UserEntity]:
        like_pattern = f"%{pattern}%"
        return db.query(UserEntity).filter(
            or_(
                UserEntity.fname.ilike(like_pattern),
                UserEntity.lname.ilike(like_pattern)
            )
        ).all()

    def update(self, db: Session, id: int, update_data: dict) -> Optional[UserEntity]:
        user = db.query(UserEntity).filter(UserEntity.id == id).first()
        
        if not user:
            return None
        
        for key, value in update_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
                
        db.commit()
        db.refresh()
        return user
    
    def delete(self, db: Session, id: int) -> bool:
        user = db.query(UserEntity).filter(UserEntity.id == id).first()
        if not user:
            return False
        
        db.delete(user)
        db.commit()
        
        return True

