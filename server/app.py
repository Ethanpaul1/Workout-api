from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError

try:
    from .models import db, Exercise, Workout, WorkoutExercise
    from .schemas import (
        exercise_schema, exercises_schema,
        workout_schema, workouts_schema,
        workout_exercise_schema,
    )
except ImportError:
    from models import db, Exercise, Workout, WorkoutExercise
    from schemas import (
        exercise_schema, exercises_schema,
        workout_schema, workouts_schema,
        workout_exercise_schema,
    )

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)


def error_response(message, status_code):
    """Helper: return a JSON-formatted error with the given message and status."""
    return make_response(jsonify({"error": message}), status_code)


# --- Workout Endpoints ---

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error_response(f"Workout with id {id} not found.", 404)
    return make_response(jsonify(workout_schema.dump(workout)), 200)


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    if not data:
        return error_response("Request body must be JSON.", 400)

    try:
        validated = workout_schema.load(data)
    except ValidationError as e:
        return error_response(e.messages, 422)

    try:
        new_workout = Workout(
            date=validated["date"],
            duration_minutes=validated["duration_minutes"],
            notes=validated.get("notes"),
        )
        db.session.add(new_workout)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return error_response(str(e), 422)

    return make_response(jsonify(workout_schema.dump(new_workout)), 201)


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return error_response(f"Workout with id {id} not found.", 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": f"Workout {id} deleted."}), 200)


# --- Exercise Endpoints ---

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error_response(f"Exercise with id {id} not found.", 404)
    return make_response(jsonify(exercise_schema.dump(exercise)), 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()
    if not data:
        return error_response("Request body must be JSON.", 400)

    try:
        validated = exercise_schema.load(data)
    except ValidationError as e:
        return error_response(e.messages, 422)

    try:
        new_exercise = Exercise(
            name=validated["name"],
            category=validated["category"],
            equipment_needed=validated.get("equipment_needed", False),
        )
        db.session.add(new_exercise)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return error_response(str(e), 422)

    return make_response(jsonify(exercise_schema.dump(new_exercise)), 201)


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return error_response(f"Exercise with id {id} not found.", 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": f"Exercise {id} deleted."}), 200)


# --- WorkoutExercise Endpoint ---

@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def create_workout_exercise(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return error_response(f"Workout with id {workout_id} not found.", 404)

    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return error_response(f"Exercise with id {exercise_id} not found.", 404)

    data = request.get_json() or {}
    data["workout_id"] = workout_id
    data["exercise_id"] = exercise_id

    try:
        validated = workout_exercise_schema.load(data)
    except ValidationError as e:
        return error_response(e.messages, 422)

    try:
        new_we = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            reps=validated.get("reps"),
            sets=validated.get("sets"),
            duration_seconds=validated.get("duration_seconds"),
        )
        db.session.add(new_we)
        db.session.commit()
    except (ValueError, IntegrityError) as e:
        db.session.rollback()
        return error_response(str(e), 422)

    return make_response(jsonify(workout_exercise_schema.dump(new_we)), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

