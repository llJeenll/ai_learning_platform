from database.db import Base, engine, SessionLocal
from database.models import Student, Topic, Assessment, LearningResource
from agents.personalized_learning_agent import PersonalizedLearningAgent

def test_low_score_gets_foundation_recommendation():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    student = Student(
        name="Test Student",
        email="test@example.com",
        grade=8
    )
    topic = Topic(
        subject="Mathematics",
        name="Fractions",
        grade=8,
        difficulty=2
    )

    db.add_all([student, topic])
    db.flush()

    db.add(
        Assessment(
            student_id=student.id,
            topic_id=topic.id,
            score=30,
            total=100
        )
    )

    db.add(
        LearningResource(
            topic_id=topic.id,
            title="Fractions Foundation",
            resource_type="Lesson",
            url="https://example.com",
            difficulty=1
        )
    )
    db.commit()

    result = PersonalizedLearningAgent().run(db, student.id)

    assert result["recommendations"][0]["action"] == "Foundation"
    assert result["recommendations"][0]["priority"] == "high"

    db.close()
