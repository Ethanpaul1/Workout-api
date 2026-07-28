# Workout Tracker API

## Description

A RESTful backend API for a workout tracking application used by personal trainers. Built with Flask, SQLAlchemy, and Marshmallow, it allows trainers to manage reusable exercises, create dated workout sessions, and associate exercises with workouts while storing per-exercise performance data such as sets, reps, and duration.

The API enforces data integrity at three layers: database table constraints, SQLAlchemy model validations, and Marshmallow schema validations.

## Installation

### Prerequisites
- Python 3.8+
- Pipenv

### Steps

```bash
git clone https://github.com/Ethanpaul1/Workout-api.git
cd Workout-api
pipenv install
pipenv shell
flask --app server.app db upgrade head
cd server
python seed.py
```

## Running the App

```bash
cd server
flask --app app.py run --port=5555
```

The API will be available at http://localhost:5555.

## Endpoints

### Workouts

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /workouts | List all workouts |
| GET | /workouts/<id> | Get a single workout with its exercises and reps/sets/duration |
| POST | /workouts | Create a new workout |
| DELETE | /workouts/<id> | Delete a workout (cascades to its WorkoutExercise rows) |

**POST /workouts body:** {"date": "2025-06-10", "duration_minutes": 45, "notes": "optional"}

### Exercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /exercises | List all exercises |
| GET | /exercises/<id> | Get a single exercise with its associated workouts |
| POST | /exercises | Create a new exercise |
| DELETE | /exercises/<id> | Delete an exercise (cascades to its WorkoutExercise rows) |

**POST /exercises body:** {"name": "Deadlift", "category": "Strength", "equipment_needed": true}

Valid categories: Strength, Cardio, Flexibility, Balance, HIIT

### WorkoutExercises

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises | Add an exercise to a workout with performance data |

**Request body:** {"sets": 3, "reps": 12, "duration_seconds": null}
