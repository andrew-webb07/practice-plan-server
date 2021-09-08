from django.db import models
from django.db.models.deletion import CASCADE

class PlanExercise(models.Model):
    exercise = models.ForeignKey("Exercise", on_delete=CASCADE)
    practice_plan = models.ForeignKey("PracticePlan", on_delete=CASCADE)