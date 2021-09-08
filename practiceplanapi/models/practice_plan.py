from django.db import models
from django.db.models.deletion import CASCADE

class PracticePlan(models.Model):
    player = models.ForeignKey("Player", on_delete=CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)