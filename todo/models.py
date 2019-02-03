from datetime import date

from django.contrib.auth.models import User
from django.db import models
from model_utils import Choices


class UserData(models.Model):
    user = models.ForeignKey(User, editable=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True


STATUS = Choices('active', 'done')


class Task(UserData):
    text = models.CharField(max_length=1000)
    status = models.CharField(choices=STATUS, default=STATUS.active, max_length=20)
    date = models.DateField(default=date.today)

    def __str__(self):
        return self.text

    def opposite_status(self):
        return STATUS.active if self.status == STATUS.done else STATUS.done

    def is_due(self):
        return self.date < date.today()
