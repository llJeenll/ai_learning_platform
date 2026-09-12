from collections import defaultdict
from sqlalchemy.orm import Session
from database.models import Assessment, Topic

def calculate_topic_mastery(db: Session, student_id: int):
    assessments = db.query(Assessment).filter(
        Assessment.student_id == student_id
    ).all()

    scores = defaultdict(list)
    for a in assessments:
        percentage = (a.score / a.total * 100) if a.total else 0
        scores[a.topic_id].append(percentage)

    result = {}
    topics = db.query(Topic).all()

    for topic in topics:
        values = scores.get(topic.id, [])
        if not values:
            mastery = 0.0
        else:
            # Recent performance is useful, but this MVP keeps a simple weighted average.
            weights = list(range(1, len(values) + 1))
            mastery = sum(v*w for v, w in zip(values, weights)) / sum(weights)

        result[topic.id] = round(mastery, 2)

    return result

def mastery_label(score: float):
    if score < 40:
        return "Needs foundational support"
    if score < 60:
        return "Developing"
    if score < 80:
        return "Proficient"
    return "Strong"
