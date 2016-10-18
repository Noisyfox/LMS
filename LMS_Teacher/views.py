from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views.generic import ListView

from LMS.mixins import QueryMixin
from LMS.models import Unit
from LMS_Teacher.mixins import TeacherMixin


class UnitQueryMixin(QueryMixin):
    def do_query(self, request, *args, **kwargs):
        unit = get_object_or_404(Unit, Q(staff=self.request.user.teacher) & Q(pk=kwargs['unit_id']))

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


class UnitListView(TeacherMixin, ListView):
    template_name = 'LMS_Teacher/unit.html'
    context_object_name = 'units'
    allow_empty = True

    def get_queryset(self):
        return Unit.objects.filter(staff=self.request.user.teacher)


class UnitInfoView(TeacherMixin, UnitQueryMixin, DetailView):
    template_name = 'LMS_Teacher/unit_info.html'

    def get_object(self, queryset=None):
        return self.unit
