from sqlalchemy.orm import Session
from database.models import Topic, LearningResource
from services.mastery_service import calculate_topic_mastery, mastery_label

def recommend_for_student(db: Session, student_id: int, subject: str | None = None):
    mastery = calculate_topic_mastery(db, student_id)

    query = db.query(Topic)
    if subject:
        query = query.filter(Topic.subject == subject)
    topics = query.all()

    ranked = sorted(topics, key=lambda t: mastery.get(t.id, 0))

    recommendations = []

    for topic in ranked[:5]:
        score = mastery.get(topic.id, 0)

        if score < 40:
            action = "Foundation"
            priority = "high"
            reason = (
                f"Mastery is {score:.0f}%. Start with foundational explanation, "
                "worked examples, and easy practice before increasing difficulty."
            )
            target_difficulty = 1
        elif score < 60:
            action = "Guided Practice"
            priority = "high"
            reason = (
                f"Mastery is {score:.0f}%. Use guided practice and immediate feedback "
                "to close the most important knowledge gaps."
            )
            target_difficulty = 2
        elif score < 80:
            action = "Independent Practice"
            priority = "medium"
            reason = (
                f"Mastery is {score:.0f}%. Continue practice with moderately challenging "
                "questions and spaced review."
            )
            target_difficulty = 2
        else:
            action = "Challenge"
            priority = "low"
            reason = (
                f"Mastery is {score:.0f}%. Provide higher-order questions or extension "
                "activities to prevent stagnation."
            )
            target_difficulty = 3

        resource = (
            db.query(LearningResource)
            .filter(
                LearningResource.topic_id == topic.id,
                LearningResource.difficulty == target_difficulty
            )
            .first()
        )

        recommendations.append({
            "topic_id": topic.id,
            "topic": topic.name,
            "subject": topic.subject,
            "mastery": score,
            "mastery_label": mastery_label(score),
            "action": action,
            "priority": priority,
            "reason": reason,
            "resource_id": resource.id if resource else None,
            "resource_title": resource.title if resource else "Teacher-created activity",
            "resource_url": resource.url if resource else "#",
        })

    return recommendations
