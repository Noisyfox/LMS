import re

from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from sendfile import sendfile

from LMS.mixins import QueryMixin
from LMS.models import Unit, Material, Assignment, AssignmentFile, GradeRecord
from LMS.views import BaseTimetableView
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


class AssignmentQueryMixin(UnitQueryMixin):
    def do_query(self, request, *args, **kwargs):
        super(AssignmentQueryMixin, self).do_query(request, *args, **kwargs)

        assignment = get_object_or_404(Assignment, Q(unit=self.unit) & Q(pk=kwargs['assignment_id']))

        self._assignment = assignment

    @property
    def assignment(self):
        if not self._assignment:
            raise Http404('Unknown assignment.')

        return self._assignment

    def get_context_data(self, **kwargs):
        ctx = super(AssignmentQueryMixin, self).get_context_data(**kwargs)

        ctx['assignment'] = self._assignment

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

        for u in units:
            grade, _ = GradeRecord.objects.get_or_create(student=self.request.user.student, unit=u)
        return HttpResponseRedirect(reverse_lazy('lms_stu:unit'))


class UnitInfoView(StudentMixin, UnitQueryMixin, DetailView):
    template_name = 'LMS_Student/unit_info.html'
    context_object_name = 'grade'

    def get_object(self, queryset=None):
        return GradeRecord.objects.get(unit=self.unit, student=self.request.user.student)


class MaterialListView(StudentMixin, UnitQueryMixin, ListView):
    template_name = 'LMS_Student/unit_material.html'
    context_object_name = 'materials'
    allow_empty = True

    def get_queryset(self):
        return Material.objects.filter(unit=self.unit)


class MaterialDownloadView(StudentMixin, MaterialQueryMixin, View):
    def get(self, request, *args, **kwargs):
        return sendfile(request, self.material.file.path, attachment=True)


class AssignmentListView(StudentMixin, UnitQueryMixin, ListView):
    template_name = 'LMS_Student/unit_assignment.html'
    context_object_name = 'assignments'
    allow_empty = True

    def get_queryset(self):
        return Assignment.objects.filter(unit=self.unit)


class AssignmentFileListView(StudentMixin, AssignmentQueryMixin, ListView):
    template_name = 'LMS_Student/unit_assignment_detail.html'
    context_object_name = 'files'
    allow_empty = True

    def get_queryset(self):
        return AssignmentFile.objects.filter(Q(assignment=self.assignment) & Q(uploader=self.request.user.student))


class AssignmentSubmitView(StudentMixin, AssignmentQueryMixin, CreateView):
    template_name = 'LMS_Student/unit_assignment_submit.html'
    model = AssignmentFile
    fields = ['name', 'file']

    def form_valid(self, form):
        # TODO: check due time
        submission = form.save(commit=False)
        submission.assignment = self.assignment
        submission.uploader = self.request.user.student
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lms_stu:assignment_detail',
                            kwargs={'unit_id': self.unit.pk, 'assignment_id': self.assignment.pk})


class TimetableView(StudentMixin, BaseTimetableView):
    template_name = 'LMS_Student/timetable.html'

    def get_units(self):
        return self.request.user.student.enrolled_unit.all()


class PersonalInfoView(StudentMixin, TemplateView):
    template_name = 'LMS_Student/personal_info.html'
