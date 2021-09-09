from django.db import models
from django.db.models.deletion import CASCADE
from django.template.defaultfilters import floatformat

class Session(models.Model):
    player = models.ForeignKey("Player", on_delete=CASCADE)
    practice_plan = models.ForeignKey("PracticePlan", on_delete=CASCADE)
    length_of_session = models.IntegerField()
    date = models.DateField(auto_now=False, auto_now_add=False)
    notes = models.CharField(max_length=150)

    @property
    def length_of_each_exercise(self):
        """Length in minutes of each exercise in practice session"""
        exercise_length = self.length_of_session / self.practice_plan.exercises.count()
        # Remove decimal
        return floatformat(exercise_length, 0)