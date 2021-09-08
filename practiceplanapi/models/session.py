from django.db import models
from django.db.models.deletion import CASCADE
from .exercise import Exercise

class Session(models.Model):
    player = models.ForeignKey("Player", on_delete=CASCADE)
    practice_plan = models.ForeignKey("PracticePlan", on_delete=CASCADE)
    length_of_session = models.IntegerField()
    date = models.DateField(auto_now=False, auto_now_add=False)
    notes = models.CharField(max_length=150)

    # @property
    # def length_of_each_exercise(self):
    #     """Length of each exercise in practice session"""
    #     exercises = Exercise.objects.filter(game=self)

    #     exercise_length = session.length_of_session / len(exercises)
        
    #     return exercise_length