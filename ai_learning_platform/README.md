# AI-Powered Personalized Learning & Teacher Assistant Platform

A lightweight MVP focused on the **Personalized Learning Recommendation Agent** for schools.

## What this MVP does

### Student side
- Student profile and class/grade
- Subject/topic selection
- Diagnostic quiz
- Skill-level estimation
- Personalized learning recommendations
- Recommended content/resources
- Difficulty adaptation
- Learning history

### Teacher side
- Dashboard of students
- Students needing support
- Topic-wise class performance
- Add assessment results
- Basic actionable recommendations

### Agentic flow
1. Collect student profile + assessment data
2. Estimate mastery for each topic
3. Detect weak/strong topics
4. Select next learning action
5. Adapt difficulty
6. Generate an explanation/recommendation
7. Save the recommendation and learning event

## Why this architecture

This version intentionally avoids heavy multi-agent frameworks, paid APIs, and local LLMs.
For an 8 GB RAM laptop, a deterministic recommendation engine + lightweight ML/ranking is
a better first implementation. LLM/RAG can be added later as an optional layer.

## Stack

- Python 3.10+
- Streamlit
- FastAPI
- SQLite
- SQLAlchemy
- scikit-learn
- pandas
- pydantic

## Run

### Windows

```powershell
cd ai_learning_platform
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts\seed_data.py
streamlit run app.py
```

Open the URL shown by Streamlit.

### API (optional)

In another terminal:

```powershell
cd ai_learning_platform
.venv\Scripts\activate
uvicorn api.main:app --reload
```

API docs:
`http://127.0.0.1:8000/docs`

## Demo accounts

Teacher:
- email: teacher@demo.local

Students:
- email: student1@demo.local
- email: student2@demo.local
- email: student3@demo.local

No real authentication is implemented in this MVP. This is a portfolio/demo project.

## Project structure

```text
ai_learning_platform/
├── app.py
├── requirements.txt
├── .env.example
├── README.md
├── data/
│   └── seed_resources.csv
├── database/
│   ├── __init__.py
│   ├── db.py
│   └── models.py
├── agents/
│   ├── __init__.py
│   └── personalized_learning_agent.py
├── services/
│   ├── __init__.py
│   ├── mastery_service.py
│   ├── recommendation_service.py
│   └── analytics_service.py
├── api/
│   ├── __init__.py
│   └── main.py
├── ui/
│   ├── __init__.py
│   ├── student_view.py
│   └── teacher_view.py
├── scripts/
│   ├── __init__.py
│   └── seed_data.py
└── tests/
    ├── __init__.py
    └── test_recommendation.py
```

## Important next upgrades

For a real deployment, add:
- proper authentication/authorization
- Gujarati content and Gujarati NLP
- teacher-approved content
- real school datasets with consent/privacy controls
- PostgreSQL
- audit logging
- evaluation metrics
- human review before high-impact recommendations
- optional LLM lesson/content generation
- RAG over approved curriculum material
