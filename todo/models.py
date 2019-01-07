from django.contrib.auth.models import User
from django.db import models


class UserData(models.Model):
    user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class Task(UserData):
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text
