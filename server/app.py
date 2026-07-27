from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate

from models import db, Exercise, Workout, WorkoutExercise

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)


# --- Workout Endpoints ---

@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    result = [{"id": w.id, "date": str(w.date), "duration_minutes": w.duration_minutes} for w in workouts]
    return make_response(jsonify(result), 200)


@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    result = {"id": workout.id, "date": str(workout.date), "duration_minutes": workout.duration_minutes}
    return make_response(jsonify(result), 200)


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()
    new_workout = Workout(
        date=data.get("date"),
        duration_minutes=data.get("duration_minutes"),
        notes=data.get("notes"),
    )
    db.session.add(new_workout)
    db.session.commit()
    return make_response(jsonify({"id": new_workout.id}), 201)


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({"error": "Workout not found"}), 404)
    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({"message": f"Workout {id} deleted."}), 200)


# --- Exercise Endpoints ---

@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    result = [{"id": e.id, "name": e.name, "category": e.category} for e in exercises]
    return make_response(jsonify(result), 200)


@app.route("/exercises/<int:id>", methods=["GET"])
def get_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    result = {"id": exercise.id, "name": exercise.name, "category": exercise.category}
    return make_response(jsonify(result), 200)


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()
    new_exercise = Exercise(
        name=data.get("name"),
        category=data.get("category"),
        equipment_needed=data.get("equipment_needed", False),
    )
    db.session.add(new_exercise)
    db.session.commit()
    return make_response(jsonify({"id": new_exercise.id}), 201)


@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({"error": "Exercise not found"}), 404)
    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({"message": f"Exercise {id} deleted."}), 200)


# --- WorkoutExercise Endpoint ---

@app.route("/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises", methods=["POST"])
def create_workout_exercise(workout_id, exercise_id):
    workout = db.session.get(Workout, workout_id)
    exercise = db.session.get(Exercise, exercise_id)
    if not workout or not exercise:
        return make_response(jsonify({"error": "Workout or Exercise not found"}), 404)

    data = request.get_json() or {}
    new_we = WorkoutExercise(
        workout_id=workout_id,
        exercise_id=exercise_id,
        reps=data.get("reps"),
        sets=data.get("sets"),
        duration_seconds=data.get("duration_seconds"),
    )
    db.session.add(new_we)
    db.session.commit()
    return make_response(jsonify({"id": new_we.id}), 201)


if __name__ == '__main__':
    app.run(port=5555, debug=True)

