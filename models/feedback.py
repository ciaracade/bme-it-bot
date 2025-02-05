from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class SolutionFeedback(Base):
    __tablename__ = 'solution_feedback'

    id = Column(Integer, primary_key=True)
    solution_id = Column(Integer, ForeignKey('solutions.id'))
    ticket_id = Column(String(50))
    was_helpful = Column(Boolean)
    feedback_text = Column(Text, nullable=True)
    user_email = Column(String(200))
    created_at = Column(DateTime, default=datetime.utcnow)

    solution = relationship("Solution", back_populates="feedback") 