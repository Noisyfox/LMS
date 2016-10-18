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


TITLES = (
    ('Mr', 'Mr'),
    ('Mrs', 'Mrs'),
    ('Ms', 'Ms'),
    ('Miss', 'Miss'),
    ('Prof', 'Prof'),
    ('Dr', 'Dr'),
)


class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDERS)
    title = models.CharField(max_length=32, choices=TITLES)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Unit(models.Model):
    name = models.CharField(max_length=128)
    year = models.IntegerField()
    session = models.IntegerField(choices=((1, 'S1'), (2, 'S2')))
    credit_point = models.FloatField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=512)

    staff = models.ManyToManyField(Teacher, through='UnitAllocation')

    def __str__(self):
        return self.name


class UnitAllocation(models.Model):
    ROLES = (
        ('c', 'Coordinator'),
        ('l', 'Lecturer'),
        ('t', 'Tutor')
    )
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    role = models.CharField(max_length=1, choices=ROLES)

    def __str__(self):
        return '%s as %s' % (self.teacher.user.username, self.get_role_display())


class Material(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    uploader = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    file = models.FileField()
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
