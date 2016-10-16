from django.conf import settings
from django.db import models


# Create your models here.


class Faculty(models.Model):
    name = models.CharField(max_length=128)
    location = models.CharField(max_length=512)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=128)
    degree = models.CharField(max_length=128)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


GENDERS = (
    ('m', 'Male'),
    ('f', 'Female'),
)


class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDERS)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    year = models.IntegerField()
    start_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDERS)
    title = models.CharField(max_length=32)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Unit(models.Model):
    name = models.CharField(max_length=128)
    coordinator = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    year = models.IntegerField()
    session = models.IntegerField(choices=((1, 'S1'), (2, 'S2')))
    credit_point = models.FloatField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=512)
