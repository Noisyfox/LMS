from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from LMS.mixins import QueryMixin
from LMS.models import Unit, Material
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


class MaterialQueryMixin(UnitQueryMixin):
    def do_query(self, request, *args, **kwargs):
        super(MaterialQueryMixin, self).do_query(request, *args, **kwargs)

        material = get_object_or_404(Material, Q(unit=self.unit) & Q(pk=kwargs['material_id']))

        self._material = material

    @property
    def material(self):
        if not self._material:
            raise Http404('Unknown material.')

        return self._material

    def get_context_data(self, **kwargs):
        ctx = super(MaterialQueryMixin, self).get_context_data(**kwargs)

        ctx['material'] = self._material

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


class MaterialListView(TeacherMixin, UnitQueryMixin, ListView):
    template_name = 'LMS_Teacher/unit_material.html'
    context_object_name = 'materials'
    allow_empty = True

    def get_queryset(self):
        return Material.objects.filter(unit=self.unit)


class MaterialCreateView(TeacherMixin, UnitQueryMixin, CreateView):
    template_name = 'LMS_Teacher/unit_material_edit.html'
    model = Material
    fields = ['name', 'file']

    def form_valid(self, form):
        mat = form.save(commit=False)
        mat.unit = self.unit
        mat.uploader = self.request.user.teacher
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lms_tec:material', kwargs={'unit_id': self.unit.pk})


class MaterialEditView(TeacherMixin, MaterialQueryMixin, UpdateView):
    template_name = 'LMS_Teacher/unit_material_edit.html'
    model = Material
    fields = ['name', 'file']

    def get_object(self, queryset=None):
        return self.material

    def get_success_url(self):
        return reverse_lazy('lms_tec:material', kwargs={'unit_id': self.unit.pk})


class MaterialDeleteView(TeacherMixin, MaterialQueryMixin, DeleteView):
    template_name = 'LMS_Teacher/unit_material_delete.html'

    def get_object(self, queryset=None):
        return self.material

    def get_success_url(self):
        return reverse_lazy('lms_tec:material', kwargs={'unit_id': self.unit.pk})
