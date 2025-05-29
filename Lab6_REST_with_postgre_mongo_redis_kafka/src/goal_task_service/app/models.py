from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.database import Base


class Goal(Base):
    __tablename__ = 'goals'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)
    text = Column(String, nullable=False)
    owner_nick = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # один goal -> много tasks
    tasks = relationship('Task', back_populates='goal', cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)
    text = Column(String, nullable=False)
    owner_nick = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    files = Column(MutableDict.as_mutable(JSON), nullable=True)

    goal_id = Column(Integer, ForeignKey('goals.id'))
    
    # одна задача -> принадлежит одной цели
    goal = relationship('Goal', back_populates='tasks')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.text,
            'owner_nick': self.owner_nick,
            'files': self.files,
            'goal_id': self.goal_id if hasattr(self, 'goal_id') else None,
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None
        }
