from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from database.db import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    email = Column(String(200), unique=True, nullable=False)
    grade = Column(Integer, nullable=False)
    medium = Column(String(50), default="English")
    created_at = Column(DateTime, default=datetime.utcnow)

class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    subject = Column(String(100), nullable=False)
    name = Column(String(150), nullable=False)
    grade = Column(Integer, nullable=False)
    difficulty = Column(Integer, default=2)
    description = Column(Text, default="")

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    score = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    time_seconds = Column(Integer, default=0)
    completed_at = Column(DateTime, default=datetime.utcnow)

class LearningResource(Base):
    __tablename__ = "learning_resources"

    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    title = Column(String(200), nullable=False)
    resource_type = Column(String(50), default="Practice")
    url = Column(String(500), default="#")
    difficulty = Column(Integer, default=2)
    language = Column(String(50), default="English")
    estimated_minutes = Column(Integer, default=15)

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    topic_id = Column(Integer, ForeignKey("topics.id"), nullable=False)
    action = Column(String(100), nullable=False)
    reason = Column(Text, nullable=False)
    priority = Column(String(30), default="medium")
    resource_id = Column(Integer, ForeignKey("learning_resources.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed = Column(Boolean, default=False)
