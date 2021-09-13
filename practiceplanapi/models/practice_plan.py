from django.db import models
from django.db.models.deletion import CASCADE

class PracticePlan(models.Model):
    player = models.ForeignKey("Player", on_delete=CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    exercises = models.ManyToManyField("Exercise", through="PlanExercise", related_name="exercises")

    @property
    def is_creator(self):
        return self.__is_creator
    @is_creator.setter
    def is_creator(self, value):
        self.__is_creator = value