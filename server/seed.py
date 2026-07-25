#!/usr/bin/env python3

from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print('Clearing existing data...')
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    print('Seeding exercises...')
    push_up = Exercise(name='Push Up', category='Strength', equipment_needed=False)
    squat = Exercise(name='Squat', category='Strength', equipment_needed=False)
    running = Exercise(name='Running', category='Cardio', equipment_needed=False)
    yoga = Exercise(name='Yoga Stretch', category='Flexibility', equipment_needed=True)

    db.session.add_all([push_up, squat, running, yoga])
    db.session.commit()

    print('Seeding workouts...')
    workout1 = Workout(
        date=date(2026, 7, 20),
        duration_minutes=45,
        notes='Morning strength session'
    )
    workout2 = Workout(
        date=date(2026, 7, 22),
        duration_minutes=30,
        notes='Cardio day'
    )

    db.session.add_all([workout1, workout2])
    db.session.commit()

    print('Seeding workout_exercises (linking workouts to exercises)...')
    we1 = WorkoutExercise(workout_id=workout1.id, exercise_id=push_up.id, reps=15, sets=3)
    we2 = WorkoutExercise(workout_id=workout1.id, exercise_id=squat.id, reps=12, sets=4)
    we3 = WorkoutExercise(workout_id=workout2.id, exercise_id=running.id, duration_seconds=1800)

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print('Done seeding!')