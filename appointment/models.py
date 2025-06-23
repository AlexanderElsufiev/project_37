
from django.db import models
from datetime import datetime

# Это модель записи на приём к кому угодно
class Appointment(models.Model):
    date = models.DateField(default=datetime.utcnow,)
    client_name = models.CharField(max_length=200)
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'

