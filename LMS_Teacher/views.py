from django.shortcuts import render
from django.views.generic import ListView

from LMS.models import Unit
from LMS_Teacher.mixins import TeacherMixin


class UnitListView(TeacherMixin, ListView):
    template_name = 'LMS_Teacher/unit.html'
    context_object_name = 'units'
    allow_empty = True

    def get_queryset(self):
        return Unit.objects.filter(staff=self.request.user.teacher)
