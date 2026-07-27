from marshmallow import Schema, fields


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(load_default=None)
    sets = fields.Int(load_default=None)
    duration_seconds = fields.Int(load_default=None)

    # Nested summaries for when this is embedded in a Workout or Exercise response
    exercise = fields.Nested(
        lambda: ExerciseSchema(only=("id", "name", "category", "equipment_needed")),
        dump_only=True
    )
    workout = fields.Nested(
        lambda: WorkoutSchema(only=("id", "date", "duration_minutes")),
        dump_only=True
    )


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

    # Nested join-table rows — only populated when fetching a single exercise
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema(only=("id", "workout_id", "reps", "sets", "duration_seconds", "workout"))),
        dump_only=True
    )


class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str(load_default=None)

    # Nested join-table rows with embedded exercise info — detail view only
    workout_exercises = fields.List(
        fields.Nested(WorkoutExerciseSchema(only=("id", "exercise_id", "reps", "sets", "duration_seconds", "exercise"))),
        dump_only=True
    )


# Shared instances so we don't re-instantiate schemas in every route
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True, exclude=("workout_exercises",))

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True, exclude=("workout_exercises",))

workout_exercise_schema = WorkoutExerciseSchema()
