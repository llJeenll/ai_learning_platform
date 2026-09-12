from sqlalchemy.orm import Session
from services.recommendation_service import recommend_for_student

class PersonalizedLearningAgent:
    """
    Lightweight agentic decision layer.

    It observes student evidence -> reasons about mastery -> chooses an action ->
    selects an approved resource.

    This is intentionally deterministic in the first version so teachers can inspect
    why a recommendation was made.
    """

    name = "Personalized Learning Recommendation Agent"

    def run(self, db: Session, student_id: int, subject=None):
        recommendations = recommend_for_student(
            db, student_id=student_id, subject=subject
        )

        return {
            "agent": self.name,
            "student_id": student_id,
            "recommendations": recommendations,
            "next_step": (
                "Complete the highest-priority activity first, then take a short "
                "assessment so the agent can update mastery."
            ),
        }
