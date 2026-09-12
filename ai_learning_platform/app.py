import streamlit as st
from database.db import init_db, SessionLocal
from database.models import Student
from agents.personalized_learning_agent import PersonalizedLearningAgent
from services.analytics_service import student_summary, students_needing_support

st.set_page_config(
    page_title="AI Learning Platform",
    page_icon="🎓",
    layout="wide"
)

init_db()

st.title("🎓 AI-Powered Personalized Learning Platform")
st.caption("MVP — Personalized Learning Recommendation Agent")

db = SessionLocal()

students = db.query(Student).order_by(Student.name).all()

if not students:
    st.warning("No data found. Run: python scripts/seed_data.py")
    db.close()
    st.stop()

role = st.sidebar.selectbox("View", ["Student", "Teacher"])

if role == "Student":
    st.sidebar.header("Student")
    selected = st.sidebar.selectbox(
        "Select demo student",
        students,
        format_func=lambda s: f"{s.name} — Grade {s.grade}"
    )

    st.header(f"Welcome, {selected.name} 👋")
    st.write(f"Grade {selected.grade} · Medium: {selected.medium}")

    rows = student_summary(db, selected.id)

    st.subheader("Your learning profile")
    cols = st.columns(min(5, len(rows)))
    for i, row in enumerate(rows[:5]):
        with cols[i]:
            st.metric(row["topic"], f"{row['mastery']:.0f}%")

    st.divider()
    st.subheader("🤖 Personalized Learning Recommendation Agent")

    agent = PersonalizedLearningAgent()
    result = agent.run(db, selected.id)

    for rec in result["recommendations"]:
        with st.container(border=True):
            c1, c2, c3 = st.columns([2, 1, 1])
            c1.markdown(f"### {rec['topic']}")
            c1.write(rec["reason"])
            c2.metric("Mastery", f"{rec['mastery']:.0f}%")
            c2.write(rec["mastery_label"])
            c3.write(f"**Action:** {rec['action']}")
            c3.write(f"**Priority:** {rec['priority'].title()}")
            st.write(f"📚 **Recommended:** {rec['resource_title']}")
            if rec["resource_url"] != "#":
                st.link_button("Open resource", rec["resource_url"])

    st.info(result["next_step"])

else:
    st.header("👩‍🏫 Teacher Dashboard")

    support = students_needing_support(db)

    c1, c2 = st.columns(2)
    c1.metric("Students", len(students))
    c2.metric("Students needing support", len(support))

    st.subheader("Students needing additional support")
    if support:
        st.dataframe(support, use_container_width=True, hide_index=True)
    else:
        st.success("No students currently below the support threshold.")

    st.subheader("Student performance")
    selected = st.selectbox(
        "Inspect student",
        students,
        format_func=lambda s: f"{s.name} — Grade {s.grade}"
    )

    rows = student_summary(db, selected.id)
    st.dataframe(rows, use_container_width=True, hide_index=True)

    st.subheader("Teacher action")
    st.write(
        "Prioritize students with low mastery, review the agent's explanation, "
        "and approve/adapt the recommended activity before assigning it."
    )

db.close()
