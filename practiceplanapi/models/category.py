from django.db import models
from django.db import models
from django.db.models.deletion import CASCADE

class Category(models.Model):
    player = models.ForeignKey("Player", on_delete=CASCADE)
    label = models.CharField(max_length=50)