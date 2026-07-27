#!/usr/bin/env python3
"""
seed.py — Populates the database with example data for all three models.
Safe to re-run: clears existing data before inserting fresh records.
"""

from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():

    # Clear existing data first (join table before parent tables,
    # otherwise foreign key constraints will block the delete)
    print("Clearing existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    # --- Exercises ---
    print("Seeding exercises...")
    push_up      = Exercise(name="Push-Up",      category="Strength",    equipment_needed=False)
    squat        = Exercise(name="Squat",         category="Strength",    equipment_needed=False)
    bench_press  = Exercise(name="Bench Press",   category="Strength",    equipment_needed=True)
    treadmill    = Exercise(name="Treadmill Run", category="Cardio",      equipment_needed=True)
    jump_rope    = Exercise(name="Jump Rope",      category="Cardio",      equipment_needed=True)
    yoga_stretch = Exercise(name="Yoga Stretch",  category="Flexibility", equipment_needed=False)
    plank        = Exercise(name="Plank",         category="Balance",     equipment_needed=False)
    burpee       = Exercise(name="Burpee",        category="HIIT",       equipment_needed=False)

    db.session.add_all([push_up, squat, bench_press, treadmill, jump_rope, yoga_stretch, plank, burpee])
    db.session.commit()

    # --- Workouts ---
    print("Seeding workouts...")
    workout1 = Workout(date=date(2025, 6, 1), duration_minutes=45, notes="Upper body strength.")
    workout2 = Workout(date=date(2025, 6, 3), duration_minutes=30, notes="Quick cardio blast.")
    workout3 = Workout(date=date(2025, 6, 5), duration_minutes=60, notes="Full-body HIIT.")
    workout4 = Workout(date=date(2025, 6, 7), duration_minutes=20, notes="Recovery and stretching.")

    db.session.add_all([workout1, workout2, workout3, workout4])
    db.session.commit()

    # --- WorkoutExercises (linking workouts to exercises) ---
    print("Seeding workout exercises...")
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=push_up.id,     sets=4, reps=15)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=bench_press.id, sets=3, reps=10)
    we3 = WorkoutExercise(workout_id=workout1.id, exercise_id=plank.id,       sets=3, duration_seconds=60)

    we4 = WorkoutExercise(workout_id=workout2.id, exercise_id=treadmill.id, duration_seconds=1200)
    we5 = WorkoutExercise(workout_id=workout2.id, exercise_id=jump_rope.id, sets=5, duration_seconds=60)

    we6 = WorkoutExercise(workout_id=workout3.id, exercise_id=burpee.id,    sets=4, reps=20)
    we7 = WorkoutExercise(workout_id=workout3.id, exercise_id=squat.id,     sets=4, reps=20)
    we8 = WorkoutExercise(workout_id=workout3.id, exercise_id=push_up.id,   sets=3, reps=15)

    we9  = WorkoutExercise(workout_id=workout4.id, exercise_id=yoga_stretch.id, duration_seconds=600)
    we10 = WorkoutExercise(workout_id=workout4.id, exercise_id=plank.id,        sets=2, duration_seconds=45)

    db.session.add_all([we1, we2, we3, we4, we5, we6, we7, we8, we9, we10])
    db.session.commit()

    print(f"\n✅ Done! Exercises: {Exercise.query.count()}, "
          f"Workouts: {Workout.query.count()}, "
          f"WorkoutExercises: {WorkoutExercise.query.count()}")
