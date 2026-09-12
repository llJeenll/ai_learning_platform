from fastapi import FastAPI, HTTPException
from database.db import init_db, SessionLocal
from database.models import Student
from agents.personalized_learning_agent import PersonalizedLearningAgent

app = FastAPI(
    title="AI Personalized Learning API",
    version="0.1.0"
)

init_db()

@app.get("/")
def root():
    return {
        "message": "AI Personalized Learning API",
        "docs": "/docs"
    }

@app.get("/students")
def list_students():
    db = SessionLocal()
    try:
        return [
            {
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "grade": s.grade,
                "medium": s.medium
            }
            for s in db.query(Student).all()
        ]
    finally:
        db.close()

@app.get("/students/{student_id}/recommendations")
def recommendations(student_id: int, subject: str | None = None):
    db = SessionLocal()
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        agent = PersonalizedLearningAgent()
        return agent.run(db, student_id, subject)
    finally:
        db.close()
