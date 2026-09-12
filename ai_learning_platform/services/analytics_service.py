from sqlalchemy.orm import Session
from sqlalchemy import func
from database.models import Student, Assessment, Topic
from services.mastery_service import calculate_topic_mastery

def student_summary(db: Session, student_id: int):
    mastery = calculate_topic_mastery(db, student_id)
    topic_rows = db.query(Topic).all()

    rows = []
    for topic in topic_rows:
        rows.append({
            "topic": topic.name,
            "subject": topic.subject,
            "mastery": mastery.get(topic.id, 0),
        })
    return rows

def students_needing_support(db: Session, threshold: float = 60):
    students = db.query(Student).all()
    result = []

    for student in students:
        mastery = calculate_topic_mastery(db, student.id)
        weak = [
            (topic_id, score)
            for topic_id, score in mastery.items()
            if 0 < score < threshold
        ]
        if weak:
            avg = sum(score for _, score in weak) / len(weak)
            result.append({
                "student_id": student.id,
                "student": student.name,
                "weak_topics": len(weak),
                "average_weak_score": round(avg, 1)
            })

    return sorted(result, key=lambda x: x["average_weak_score"])
