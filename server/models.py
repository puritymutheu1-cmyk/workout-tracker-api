from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

ALLOWED_CATEGORIES = ['Cardio', 'Strength', 'Flexibility', 'Balance']


class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    # An Exercise has many WorkoutExercises
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='exercise',
        cascade='all, delete-orphan'
    )
    # An Exercise has many Workouts through WorkoutExercises
    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises',
        viewonly=True
    )

    # --- Table constraint #1: category must be one of an allowed set ---
    __table_args__ = (
        CheckConstraint(
            "category IN ('Cardio', 'Strength', 'Flexibility', 'Balance')",
            name='valid_category'
        ),
    )

    # --- Model validation #1: name can't be blank ---
    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError('Exercise name cannot be blank')
        return name.strip()

    # --- Model validation #2: category must be a known value ---
    @validates('category')
    def validate_category(self, key, category):
        if category not in ALLOWED_CATEGORIES:
            raise ValueError(f'category must be one of {ALLOWED_CATEGORIES}')
        return category

    def __repr__(self):
        return f'<Exercise {self.id}: {self.name} ({self.category})>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    # A Workout has many WorkoutExercises
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )
    # A Workout has many Exercises through WorkoutExercises
    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        back_populates='workouts',
        viewonly=True
    )

    # --- Table constraint #2: duration must be positive ---
    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='positive_duration'),
    )

    # --- Model validation #3: duration must be a positive integer ---
    @validates('duration_minutes')
    def validate_duration(self, key, duration_minutes):
        if duration_minutes is None or duration_minutes <= 0:
            raise ValueError('duration_minutes must be a positive integer')
        return duration_minutes

    def __repr__(self):
        return f'<Workout {self.id} on {self.date}, {self.duration_minutes} min>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    # A WorkoutExercise belongs to a Workout
    workout = db.relationship('Workout', back_populates='workout_exercises')
    # A WorkoutExercise belongs to an Exercise
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    # --- Table constraints #3 and #4: reps/sets can't be negative or zero ---
    __table_args__ = (
        CheckConstraint('reps IS NULL OR reps > 0', name='positive_reps'),
        CheckConstraint('sets IS NULL OR sets > 0', name='positive_sets'),
    )

    # --- Model validation #4: numeric fields can't be negative ---
    @validates('reps', 'sets', 'duration_seconds')
    def validate_non_negative(self, key, value):
        if value is not None and value <= 0:
            raise ValueError(f'{key} must be a positive number')
        return value

    def __repr__(self):
        return f'<WorkoutExercise {self.id}: workout={self.workout_id} exercise={self.exercise_id}>'