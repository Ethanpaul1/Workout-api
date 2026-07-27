from marshmallow import Schema, fields, validate, validates, ValidationError
from datetime import date


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(load_default=None)
    sets = fields.Int(load_default=None)
    duration_seconds = fields.Int(load_default=None)

    # Use lambdas so these nested schemas can reference each other without circular import issues.
    exercise = fields.Nested(
        lambda: ExerciseSchema(only=("id", "name", "category", "equipment_needed")),
        dump_only=True
    )
    workout = fields.Nested(
        lambda: WorkoutSchema(only=("id", "date", "duration_minutes")),
        dump_only=True
    )

    # --- Schema Validations ---
    @validates("sets")
    def validate_sets(self, value, **kwargs):
        if value is not None and value < 1:
            raise ValidationError("sets must be a positive integer (>= 1).")

    @validates("reps")
    def validate_reps(self, value, **kwargs):
        if value is not None and value < 1:
            raise ValidationError("reps must be a positive integer (>= 1).")

    @validates("duration_seconds")
    def validate_duration_seconds(self, value, **kwargs):
        if value is not None and value < 1:
            raise ValidationError("duration_seconds must be a positive integer (>= 1).")


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, error="Exercise name cannot be empty.")
    )
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema(only=("id", "workout_id", "reps", "sets", "duration_seconds", "workout"))),
        dump_only=True
    )

    # --- Schema Validations ---
    @validates("name")
    def validate_name(self, value, **kwargs):
        if not value or not value.strip():
            raise ValidationError("Exercise name cannot be blank.")

    @validates("category")
    def validate_category(self, value, **kwargs):
        allowed = {"Strength", "Cardio", "Flexibility", "Balance", "HIIT"}
        if value not in allowed:
            raise ValidationError(f"Category must be one of: {', '.join(sorted(allowed))}.")


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(
        required=True,
        validate=validate.Range(min=1, error="duration_minutes must be at least 1.")
    )
    notes = fields.Str(load_default=None)

    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema(only=("id", "exercise_id", "reps", "sets", "duration_seconds", "exercise"))),
        dump_only=True
    )

    # --- Schema Validations ---
    @validates("duration_minutes")
    def validate_duration(self, value, **kwargs):
        if value < 1:
            raise ValidationError("duration_minutes must be at least 1 minute.")

    @validates("date")
    def validate_date(self, value, **kwargs):
        if value > date.today():
            raise ValidationError("Workout date cannot be in the future.")


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=("workout_exercises",))

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=("workout_exercises",))

workout_exercise_schema = WorkoutExerciseSchema()
