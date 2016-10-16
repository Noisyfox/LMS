from django.contrib import admin

# Register your models here.
from LMS.models import Faculty, Course

admin.site.register(Faculty)
admin.site.register(Course)
