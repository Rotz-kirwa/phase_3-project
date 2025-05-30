from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from .base import Base

class Attendance(Base):
    __tablename__ = 'attendance'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    date = Column(String, nullable=False)
    status = Column(String, nullable=False)
    
    student = relationship("Student")
    
    __table_args__ = (
        UniqueConstraint('student_id', 'date', name='_student_date_uc'),
    )
    
    def __repr__(self):
        return f"<Attendance(id={self.id}, student_id={self.student_id}, date='{self.date}', status='{self.status}')>"