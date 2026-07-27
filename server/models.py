from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from datetime import date

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)

    # Table constraints: name must exist and be unique
    name = db.Column(db.String, nullable=False, unique=True)

    # Table constraint: category must exist
    category = db.Column(db.String, nullable=False)

    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    # Delete join rows automatically when an exercise is removed so the association stays consistent.
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="exercise",
        cascade="all, delete-orphan"
    )

    # This relationship is read-only; workout rows are created through WorkoutExercise explicitly.
    workouts = db.relationship(
        "Workout",
        secondary="workout_exercises",
        back_populates="exercises",
        viewonly=True
    )

    # --- Model Validations ---
    @validates("name")
    def validate_name(self, key, value):
        if not value or not value.strip():
            raise ValueError("Exercise name cannot be empty.")
        return value.strip()

    @validates("category")
    def validate_category(self, key, value):
        allowed = {"Strength", "Cardio", "Flexibility", "Balance", "HIIT"}
        if value not in allowed:
            raise ValueError(f"Category must be one of: {', '.join(sorted(allowed))}.")
        return value

    def __repr__(self):
        return f"<Exercise id={self.id} name='{self.name}'>"


class Workout(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)

    # Table constraint: date must exist
    date = db.Column(db.Date, nullable=False)

    # Table constraint: duration must exist
    duration_minutes = db.Column(db.Integer, nullable=False)

    notes = db.Column(db.Text)

    # Delete join rows automatically when a workout is removed so the association stays consistent.
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan"
    )

    # This relationship is read-only; workout rows are created through WorkoutExercise explicitly.
    exercises = db.relationship(
        "Exercise",
        secondary="workout_exercises",
        back_populates="workouts",
        viewonly=True
    )

    # --- Model Validations ---
    @validates("duration_minutes")
    def validate_duration(self, key, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError("duration_minutes must be a positive integer (>= 1).")
        return value

    @validates("date")
    def validate_date(self, key, value):
        if value is None:
            raise ValueError("Workout date is required.")
        if isinstance(value, date) and value > date.today():
            raise ValueError("Workout date cannot be in the future.")
        return value

    def __repr__(self):
        return f"<Workout id={self.id} date='{self.date}'>"


class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    id = db.Column(db.Integer, primary_key=True)

    # Table constraints: foreign keys must exist (referential integrity)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    # --- Model Validations ---
    @validates("sets")
    def validate_sets(self, key, value):
        if value is not None and (not isinstance(value, int) or value < 1):
            raise ValueError("sets must be a positive integer.")
        return value

    @validates("reps")
    def validate_reps(self, key, value):
        if value is not None and (not isinstance(value, int) or value < 1):
            raise ValueError("reps must be a positive integer.")
        return value

    @validates("duration_seconds")
    def validate_duration_seconds(self, key, value):
        if value is not None and (not isinstance(value, int) or value < 1):
            raise ValueError("duration_seconds must be a positive integer.")
        return value

    def __repr__(self):
        return f"<WorkoutExercise id={self.id}>"
