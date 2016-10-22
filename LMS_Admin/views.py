from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.datetime_safe import date
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView

from LMS.mixins import QueryMixin
from LMS.models import Student, Teacher, Unit, UnitAllocation, Class
from LMS_Admin.forms import StudentEditForm, TeacherEditForm, ClassForm
from LMS_Admin.mixins import AdminMixin
from LMS_Admin.models import UidGen


def generate_uid(first_name, last_name):
    u = UidGen()
    u.save()

    uid = int(u.pk)

    return '%s%s%04d' % (first_name[:2].lower(), last_name[:2].lower(), uid)


class AdminStudentListView(AdminMixin, ListView):
    template_name = 'LMS_Admin/account_student.html'
    allow_empty = True
    model = Student
    context_object_name = 'students'


class StudentCreateView(AdminMixin, FormView):
    template_name = 'LMS_Admin/account_student_edit.html'
    form_class = StudentEditForm
    success_url = reverse_lazy('lms_admin:account_student')

    def get_initial(self):
        init = super().get_initial()

        init.update({
            'gender': 'm',
            'year': date.today().year
        })

        return init

    def form_valid(self, form):
        User = get_user_model()
        user = User()
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        user.username = generate_uid(first_name, last_name)
        user.first_name = first_name
        user.last_name = last_name
        user.email = form.cleaned_data['email']
        user.set_password(form.cleaned_data['password'])
        user.save()

        try:
            student = Student(user=user)
            student.gender = form.cleaned_data['gender']
            student.year = form.cleaned_data['year']
            student.course = form.cleaned_data['course']
            student.start_date = form.cleaned_data['start_date']
            student.save()
        except Exception:
            user.delete()
            raise

        return super().form_valid(form)


class StudentEditView(AdminMixin, FormView):
    template_name = 'LMS_Admin/account_student_edit.html'
    form_class = StudentEditForm
    success_url = reverse_lazy('lms_admin:account_student')

    def get_object(self):
        return Student.objects.get(pk=self.kwargs['pk'])

    def get_initial(self):
        init = super().get_initial()

        student = self.get_object()

        init.update({
            'first_name': student.user.first_name,
            'last_name': student.user.last_name,
            'gender': student.gender,
            'year': student.year,
            'course': student.course,
            'start_date': student.start_date,
            'email': student.user.email,
        })

        return init

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['password'].required = False
        return form

    def form_valid(self, form):
        student = self.get_object()
        user = student.user

        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        if 'password' in form.cleaned_data and form.cleaned_data['password']:
            user.set_password(form.cleaned_data['password'])
        user.save()

        student.gender = form.cleaned_data['gender']
        student.year = form.cleaned_data['year']
        student.course = form.cleaned_data['course']
        student.start_date = form.cleaned_data['start_date']
        student.save()

        return super().form_valid(form)


class AdminTeacherListView(AdminMixin, ListView):
    template_name = 'LMS_Admin/account_teacher.html'
    allow_empty = True
    model = Teacher
    context_object_name = 'teachers'


class TeacherCreateView(AdminMixin, FormView):
    template_name = 'LMS_Admin/account_teacher_edit.html'
    form_class = TeacherEditForm
    success_url = reverse_lazy('lms_admin:account_teacher')

    def get_initial(self):
        init = super().get_initial()

        init.update({
            'gender': 'm',
        })

        return init

    def form_valid(self, form):
        User = get_user_model()
        user = User()
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        user.username = generate_uid(first_name, last_name)
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(form.cleaned_data['password'])
        user.is_staff = True
        user.save()

        try:
            teacher = Teacher(user=user)
            teacher.title = form.cleaned_data['title']
            teacher.gender = form.cleaned_data['gender']
            teacher.faculty = form.cleaned_data['faculty']
            teacher.save()
        except Exception:
            user.delete()
            raise

        return super().form_valid(form)


class TeacherEditView(AdminMixin, FormView):
    template_name = 'LMS_Admin/account_teacher_edit.html'
    form_class = TeacherEditForm
    success_url = reverse_lazy('lms_admin:account_teacher')

    def get_object(self):
        return Teacher.objects.get(pk=self.kwargs['pk'])

    def get_initial(self):
        init = super().get_initial()

        teacher = self.get_object()

        init.update({
            'title': teacher.title,
            'first_name': teacher.user.first_name,
            'last_name': teacher.user.last_name,
            'gender': teacher.gender,
            'faculty': teacher.faculty
        })

        return init

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['password'].required = False
        return form

    def form_valid(self, form):
        teacher = self.get_object()
        user = teacher.user

        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        if 'password' in form.cleaned_data and form.cleaned_data['password']:
            user.set_password(form.cleaned_data['password'])
        user.save()

        teacher.title = form.cleaned_data['title']
        teacher.gender = form.cleaned_data['gender']
        teacher.faculty = form.cleaned_data['faculty']
        teacher.save()

        return super().form_valid(form)


class AdminUnitListView(AdminMixin, ListView):
    template_name = 'LMS_Admin/unit.html'
    allow_empty = True
    model = Unit
    context_object_name = 'units'


class UnitCreateView(AdminMixin, CreateView):
    template_name = 'LMS_Admin/unit_edit.html'
    model = Unit
    fields = ['code', 'name', 'year', 'session', 'credit_point', 'faculty', 'description', 'location']
    success_url = reverse_lazy('lms_admin:unit')

    def get_initial(self):
        init = super().get_initial()

        init.update({
            'year': date.today().year
        })

        return init


class UnitEditView(AdminMixin, UpdateView):
    template_name = 'LMS_Admin/unit_edit.html'
    model = Unit
    fields = ['code', 'name', 'year', 'session', 'credit_point', 'faculty', 'description', 'location']
    success_url = reverse_lazy('lms_admin:unit')
    pk_url_kwarg = 'unit_id'


class UnitQueryMixin(QueryMixin):
    def do_query(self, request, *args, **kwargs):
        unit = get_object_or_404(Unit, pk=kwargs['unit_id'])

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


class AllocQueryMixin(UnitQueryMixin):
    def do_query(self, request, *args, **kwargs):
        super().do_query(request, *args, **kwargs)

        alloc = get_object_or_404(UnitAllocation, pk=kwargs['alloc_id'])

        if alloc.unit != self.unit:
            raise Http404('Unknown staff.')

        self._alloc = alloc

    @property
    def allocation(self):
        if not self._alloc:
            raise Http404('Unknown staff.')

        return self._alloc

    def get_context_data(self, **kwargs):
        ctx = super(AllocQueryMixin, self).get_context_data(**kwargs)

        ctx['alloc'] = self._alloc

        return ctx


class ClassQueryMixin(UnitQueryMixin):
    def do_query(self, request, *args, **kwargs):
        super().do_query(request, *args, **kwargs)

        _class = get_object_or_404(Class, pk=kwargs['class_id'])

        if _class.unit != self.unit:
            raise Http404('Unknown class.')

        self._class = _class

    @property
    def clazz(self):
        if not self._class:
            raise Http404('Unknown staff.')

        return self._class

    def get_context_data(self, **kwargs):
        ctx = super(ClassQueryMixin, self).get_context_data(**kwargs)

        ctx['class'] = self._class

        return ctx


class StaffListView(AdminMixin, UnitQueryMixin, ListView):
    template_name = 'LMS_Admin/unit_staff.html'
    allow_empty = True
    context_object_name = 'allocations'

    def get_queryset(self):
        return UnitAllocation.objects.filter(unit=self.unit)


class StaffAddView(AdminMixin, UnitQueryMixin, CreateView):
    template_name = 'LMS_Admin/unit_staff_edit.html'
    model = UnitAllocation
    fields = ['teacher', 'role']

    def form_valid(self, form):
        allocation = form.save(commit=False)
        allocation.unit = self.unit

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lms_admin:unit_staff', kwargs={'unit_id': self.unit.pk})


class StaffEditView(AdminMixin, AllocQueryMixin, UpdateView):
    template_name = 'LMS_Admin/unit_staff_edit.html'
    model = UnitAllocation
    fields = ['teacher', 'role']

    def get_object(self, queryset=None):
        return self.allocation

    def get_success_url(self):
        return reverse_lazy('lms_admin:unit_staff', kwargs={'unit_id': self.unit.pk})


class StaffDeleteView(AdminMixin, AllocQueryMixin, DeleteView):
    template_name = 'LMS_Admin/unit_staff_delete.html'

    def get_object(self, queryset=None):
        return self.allocation

    def get_success_url(self):
        return reverse_lazy('lms_admin:unit_staff', kwargs={'unit_id': self.unit.pk})


class ClassListView(AdminMixin, UnitQueryMixin, ListView):
    template_name = 'LMS_Admin/unit_class.html'
    allow_empty = True
    context_object_name = 'classes'

    def get_queryset(self):
        return Class.objects.filter(unit=self.unit)


class ClassAddView(AdminMixin, UnitQueryMixin, CreateView):
    template_name = 'LMS_Admin/unit_class_edit.html'
    form_class = ClassForm

    def form_valid(self, form):
        _class = form.save(commit=False)
        _class.unit = self.unit

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('lms_admin:unit_class', kwargs={'unit_id': self.unit.pk})


class ClassEditView(AdminMixin, ClassQueryMixin, UpdateView):
    template_name = 'LMS_Admin/unit_class_edit.html'
    form_class = ClassForm

    def get_object(self, queryset=None):
        return self.clazz

    def get_success_url(self):
        return reverse_lazy('lms_admin:unit_class', kwargs={'unit_id': self.unit.pk})


class ClassDeleteView(AdminMixin, ClassQueryMixin, DeleteView):
    template_name = 'LMS_Admin/unit_class_delete.html'

    def get_object(self, queryset=None):
        return self.clazz

    def get_success_url(self):
        return reverse_lazy('lms_admin:unit_class', kwargs={'unit_id': self.unit.pk})
