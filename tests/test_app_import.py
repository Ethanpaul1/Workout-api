import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))


def test_app_imports_from_repo_root():
    from server.app import app

    assert app is not None
    assert any(rule.rule == "/workouts" for rule in app.url_map.iter_rules())


def test_duplicate_exercise_returns_422():
    from server.app import app
    from server.models import db

    with app.app_context():
        db.drop_all()
        db.create_all()

        client = app.test_client()
        first = client.post(
            "/exercises",
            json={"name": "Deadlift", "category": "Strength", "equipment_needed": True},
        )
        second = client.post(
            "/exercises",
            json={"name": "Deadlift", "category": "Strength", "equipment_needed": True},
        )

    assert first.status_code == 201
    assert second.status_code == 422
