from django.contrib import admin

# Register your models here.
from LMS.models import Faculty, Course, Unit, Student

admin.site.register(Faculty)
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Student)
