from django.db import models
from django.db.models.deletion import CASCADE

class Exercise(models.Model):
    player = models.ForeignKey("Player", on_delete=CASCADE)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=150)
    category = models.ForeignKey("Category", on_delete=CASCADE)
    example_picture = models.ImageField(upload_to="image", height_field=None, width_field=None, max_length=None, null=True)