from django.db import models
from django.db import models
from django.db.models.deletion import CASCADE

class Category(models.Model):
    player = models.ForeignKey("Player", on_delete=CASCADE)
    label = models.CharField(max_length=50)

    @property
    def is_creator(self):
        return self.__is_creator
    @is_creator.setter
    def is_creator(self, value):
        self.__is_creator = value