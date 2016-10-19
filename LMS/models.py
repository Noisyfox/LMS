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

    enrolled_unit = models.ManyToManyField('Unit', blank=True)

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
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    year = models.IntegerField()
    session = models.IntegerField(choices=((1, 'S1'), (2, 'S2')))
    credit_point = models.FloatField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=512)

    staff = models.ManyToManyField(Teacher, through='UnitAllocation')

    def __str__(self):
        return '%s: %s' % (self.code, self.name)


DAY_OF_WEEK = (
    (1, 'Monday'),
    (2, 'Tuesday'),
    (3, 'Wednesday'),
    (4, 'Thursday'),
    (5, 'Friday'),
    (6, 'Saturday'),
    (7, 'Sunday'),
)


class Class(models.Model):
    TYPE = (
        ('l', 'Lecture'),
        ('t', 'Tutorial'),
        ('b', 'Laboratory')
    )
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    day = models.PositiveSmallIntegerField(choices=DAY_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_week = models.PositiveSmallIntegerField()
    end_week = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=1, choices=TYPE)
    location = models.CharField(max_length=128)

    @property
    def fine_str(self):
        return '{:%I:%M %p} to {:%I:%M %p}, weeks {}-{}: {} {} in {}' .format(
            self.start_time, self.end_time, self.start_week, self.end_week, self.unit.code, self.get_type_display(),
            self.location)


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
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Assignment(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    publish_time = models.DateTimeField(auto_now_add=True)
    due_time = models.DateTimeField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class AssignmentFile(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    uploader = models.ForeignKey(Student, on_delete=models.CASCADE)
    name = models.CharField(max_length=256)
    file = models.FileField()
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
