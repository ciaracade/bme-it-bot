from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Solution(Base):
    __tablename__ = 'solutions'

    id = Column(Integer, primary_key=True)
    ticket_id = Column(String(50))
    problem_description = Column(Text)
    solution_description = Column(Text)
    category = Column(String(100))
    keywords = Column(String(200))  # Comma-separated keywords
    success_rate = Column(Float, default=0.0)
    usage_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    source = Column(String(50))  # 'google_docs', 'ai_generated', 'manual' 