from sqlalchemy import Column, Integer, String
from app.database import Base

class UserEntity(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    nick = Column(String, unique=True, index=True)
    fname = Column(String)
    lname = Column(String)
    password = Column(String)
    role = Column(String)
    
    def __repr__(self):
        return f'User-{self.id}({self.fname} {self.lname} {self.nick})'
