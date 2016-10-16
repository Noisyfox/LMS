from django.db import models

# Create your models here.


class UidGen(models.Model):
    taken = models.BooleanField(default=True)
