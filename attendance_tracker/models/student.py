from sqlalchemy import Column, Integer, String
from .base import Base

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    
    def __repr__(self):
        return f"<Student(id={self.id}, name='{self.name}')>"