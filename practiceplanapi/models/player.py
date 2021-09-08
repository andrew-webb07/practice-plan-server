from django.db import models
from django.contrib.auth.models import User

class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    practice_focus = models.CharField(max_length=50)
    bio = models.CharField(max_length=200)
    is_public = models.BooleanField(default=False)