import re

from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView
from django.views.generic import ListView

from LMS.mixins import QueryMixin
from LMS.models import Unit
from LMS_Student.mixins import StudentMixin


class UnitQueryMixin(QueryMixin):
    def do_query(self, request, *args, **kwargs):
        unit = get_object_or_404(Unit, Q(student=self.request.user.student) & Q(pk=kwargs['unit_id']))

        self._unit = unit

    @property
    def unit(self):
        if not self._unit:
            raise Http404('Unknown unit.')

        return self._unit

    def get_context_data(self, **kwargs):
        ctx = super(UnitQueryMixin, self).get_context_data(**kwargs)

        ctx['unit'] = self._unit

        return ctx


class UnitListView(StudentMixin, ListView):
    template_name = 'LMS_Student/unit.html'
    context_object_name = 'units'
    allow_empty = True

    def get_queryset(self):
        return self.request.user.student.enrolled_unit.all()


class EnrollListView(StudentMixin, ListView):
    template_name = 'LMS_Student/enroll.html'
    context_object_name = 'units'
    allow_empty = True
    model = Unit

    def post(self, request, *args, **kwargs):
        unit_id = request.POST.getlist('unit')
        units = Unit.objects.filter(pk__in=unit_id).all()
        self.request.user.student.enrolled_unit = units
        self.request.user.student.save()
        return HttpResponseRedirect(reverse_lazy('lms_stu:unit'))


class UnitInfoView(StudentMixin, UnitQueryMixin, DetailView):
    template_name = 'LMS_Student/unit_info.html'

    def get_object(self, queryset=None):
        return self.unit
