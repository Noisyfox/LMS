from django.core.mail import send_mail
from django.db.models import Q
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.views.generic import UpdateView

from LMS.mixins import QueryMixin
from LMS.models import Unit, Material, Assignment, AssignmentFile, GradeRecord, Student
from LMS.views import BaseTimetableView
from LMS_Teacher.forms import AssignmentForm, GradeEditForm, GradeRecordForm
from LMS_Teacher.mixins import TeacherMixin


class UnitQueryMixin(QueryMixin):
    def do_query(self, request, *args, **kwargs):
        unit = get_object_or_404(self.request.user.teacher.unit_set.distinct(), pk=kwargs['unit_id'])

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


class UnitListView(TeacherMixin, ListView):
    template_name = 'LMS_Teacher/unit.html'
    context_object_name = 'units'
    allow_empty = True

    def get_queryset(self):
        return self.request.user.teacher.unit_set.distinct()


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
    fields = ['name', 'description', 'file']

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
    fields = ['name', 'description', 'file']

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


class AssignmentListView(TeacherMixin, UnitQueryMixin, ListView):
    template_name = 'LMS_Teacher/unit_assignment.html'
    context_object_name = 'assignments'
    allow_empty = True

    def get_queryset(self):
        return Assignment.objects.filter(unit=self.unit)


class AssignmentCreateView(TeacherMixin, UnitQueryMixin, CreateView):
    template_name = 'LMS_Teacher/unit_assignment_edit.html'
    form_class = AssignmentForm

    def form_valid(self, form):
        mat = form.save(commit=False)
        mat.unit = self.unit
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lms_tec:assignment', kwargs={'unit_id': self.unit.pk})


class AssignmentEditView(TeacherMixin, AssignmentQueryMixin, UpdateView):
    template_name = 'LMS_Teacher/unit_assignment_edit.html'
    form_class = AssignmentForm

    def get_object(self, queryset=None):
        return self.assignment

    def get_success_url(self):
        return reverse_lazy('lms_tec:assignment', kwargs={'unit_id': self.unit.pk})


class AssignmentDeleteView(TeacherMixin, AssignmentQueryMixin, DeleteView):
    template_name = 'LMS_Teacher/unit_assignment_delete.html'

    def get_object(self, queryset=None):
        return self.assignment

    def get_success_url(self):
        return reverse_lazy('lms_tec:assignment', kwargs={'unit_id': self.unit.pk})


class AssignmentFileListView(TeacherMixin, AssignmentQueryMixin, ListView):
    template_name = 'LMS_Teacher/unit_assignment_file.html'
    context_object_name = 'files'
    allow_empty = True

    def get_queryset(self):
        return AssignmentFile.objects.filter(assignment=self.assignment)


class TimetableView(TeacherMixin, BaseTimetableView):
    template_name = 'LMS_Teacher/timetable.html'

    def get_units(self):
        return self.request.user.teacher.unit_set.all()


class UnitGradeView(TeacherMixin, UnitQueryMixin, ListView):
    template_name = 'LMS_Teacher/unit_grade.html'
    context_object_name = 'records'

    def get_queryset(self):
        return GradeRecord.objects.filter(Q(unit=self.unit) & Q(student__in=self.unit.student_set.all()))


class UnitGradeEditView(TeacherMixin, UnitQueryMixin, UpdateView):
    template_name = 'LMS_Teacher/unit_grade_edit.html'
    form_class = GradeEditForm

    def get_object(self, queryset=None):
        return self.unit

    def get_success_url(self):
        return reverse_lazy('lms_tec:grade', kwargs={'unit_id': self.unit.pk})


class UnitGradeMarkView(TeacherMixin, UnitQueryMixin, UpdateView):
    template_name = 'LMS_Teacher/unit_grade_edit.html'
    form_class = GradeRecordForm

    def get_object(self, queryset=None):
        return GradeRecord.objects.get(
            Q(unit=self.unit) & Q(student__in=self.unit.student_set.all()) & Q(pk=self.kwargs['record_id']))

    def get_success_url(self):
        return reverse_lazy('lms_tec:grade', kwargs={'unit_id': self.unit.pk})


class UnitEmailView(TeacherMixin, UnitQueryMixin, ListView):
    template_name = 'LMS_Teacher/unit_email.html'
    context_object_name = 'students'
    allow_empty = True

    def get_queryset(self):
        return self.unit.student_set.all()

    def post(self, request, *args, **kwargs):
        student_id = request.POST.getlist('student')
        subject = request.POST['subject']
        content = request.POST['mail_content']

        recipient = [s.user.email for s in Student.objects.filter(pk__in=student_id)]

        send_mail(subject, content, 'teacher@lms.com', recipient)

        return HttpResponseRedirect(reverse_lazy('lms_tec:email', kwargs={'unit_id': self.unit.pk}))


class PersonalInfoView(TeacherMixin, TemplateView):
    template_name = 'LMS_Teacher/personal_info.html'
