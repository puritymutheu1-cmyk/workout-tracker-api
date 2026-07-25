from marshmallow import Schema, fields, validate

ALLOWED_CATEGORIES = ['Cardio', 'Strength', 'Flexibility', 'Balance']


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    # Schema validation #1: name required, must not be blank
    name = fields.String(
        required=True,
        validate=validate.Length(min=1, error='Name cannot be blank')
    )
    # Schema validation #2: category must be one of the allowed values
    category = fields.String(
        required=True,
        validate=validate.OneOf(ALLOWED_CATEGORIES)
    )
    equipment_needed = fields.Boolean(load_default=False)


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(dump_only=True)
    # Schema validation #3: reps/sets/duration must be positive if provided
    reps = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    exercise = fields.Nested(ExerciseSchema, dump_only=True)


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    # Schema validation #4: duration must be a positive number
    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1))
    notes = fields.String(allow_none=True)
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)


exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()