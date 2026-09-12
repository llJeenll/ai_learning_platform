from database.db import Base, engine, SessionLocal
from database.models import Student, Topic, LearningResource, Assessment

def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    students = [
        Student(name="Aarav Patel", email="student1@demo.local", grade=8, medium="English"),
        Student(name="Diya Shah", email="student2@demo.local", grade=8, medium="Gujarati"),
        Student(name="Ravi Parmar", email="student3@demo.local", grade=8, medium="English"),
    ]
    db.add_all(students)
    db.flush()

    topics = [
        Topic(subject="Mathematics", name="Fractions", grade=8, difficulty=2,
              description="Equivalent fractions, operations and applications."),
        Topic(subject="Mathematics", name="Linear Equations", grade=8, difficulty=2,
              description="Solve one-variable linear equations."),
        Topic(subject="Science", name="Force and Motion", grade=8, difficulty=2,
              description="Force, motion, speed and simple applications."),
        Topic(subject="Science", name="Light", grade=8, difficulty=2,
              description="Reflection and basic properties of light."),
        Topic(subject="English", name="Reading Comprehension", grade=8, difficulty=2,
              description="Understand passages, inference and vocabulary."),
    ]
    db.add_all(topics)
    db.flush()

    resources = []
    for t in topics:
        resources.extend([
            LearningResource(
                topic_id=t.id,
                title=f"{t.name}: Foundation Lesson",
                resource_type="Lesson",
                url="https://example.com/foundation",
                difficulty=1,
                language="English",
                estimated_minutes=15
            ),
            LearningResource(
                topic_id=t.id,
                title=f"{t.name}: Guided Practice",
                resource_type="Practice",
                url="https://example.com/guided",
                difficulty=2,
                language="English",
                estimated_minutes=20
            ),
            LearningResource(
                topic_id=t.id,
                title=f"{t.name}: Challenge Activity",
                resource_type="Challenge",
                url="https://example.com/challenge",
                difficulty=3,
                language="English",
                estimated_minutes=25
            ),
        ])
    db.add_all(resources)
    db.flush()

    # Seed assessment patterns to demonstrate personalization.
    patterns = [
        [35, 48, 72, 81, 90],  # student 1
        [25, 42, 58, 63, 70],  # student 2
        [82, 88, 76, 91, 85],  # student 3
    ]

    for student, scores in zip(students, patterns):
        for topic, score in zip(topics, scores):
            db.add(
                Assessment(
                    student_id=student.id,
                    topic_id=topic.id,
                    score=score,
                    total=100,
                    time_seconds=600
                )
            )

    db.commit()
    db.close()
    print("Database seeded successfully: learning_platform.db")

if __name__ == "__main__":
    seed()
