from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.datetime_safe import date
from django.views.generic import CreateView
from django.views.generic import FormView
from django.views.generic import ListView
from django.views.generic import UpdateView

from LMS.models import Student, Teacher, Unit
from LMS_Admin.forms import StudentEditForm, TeacherEditForm
from LMS_Admin.models import UidGen


def generate_uid(first_name, last_name):
    u = UidGen()
    u.save()

    uid = int(u.pk)

    return '%s%s%04d' % (first_name[:2].lower(), last_name[:2].lower(), uid)


class AdminStudentListView(ListView):
    template_name = 'LMS_Admin/account_student.html'
    allow_empty = True
    model = Student
    context_object_name = 'students'


class StudentCreateView(FormView):
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


class StudentEditView(FormView):
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
        if 'password' in form.cleaned_data:
            user.set_password(form.cleaned_data['password'])
        user.save()

        student.gender = form.cleaned_data['gender']
        student.year = form.cleaned_data['year']
        student.course = form.cleaned_data['course']
        student.start_date = form.cleaned_data['start_date']
        student.save()

        return super().form_valid(form)


class AdminTeacherListView(ListView):
    template_name = 'LMS_Admin/account_teacher.html'
    allow_empty = True
    model = Teacher
    context_object_name = 'teachers'


class TeacherCreateView(FormView):
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


class TeacherEditView(FormView):
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
        if 'password' in form.cleaned_data:
            user.set_password(form.cleaned_data['password'])
        user.save()

        teacher.title = form.cleaned_data['title']
        teacher.gender = form.cleaned_data['gender']
        teacher.faculty = form.cleaned_data['faculty']
        teacher.save()

        return super().form_valid(form)


class AdminUnitListView(ListView):
    template_name = 'LMS_Admin/unit.html'
    allow_empty = True
    model = Unit
    context_object_name = 'units'


class UnitCreateView(CreateView):
    template_name = 'LMS_Admin/unit_edit.html'
    model = Unit
    fields = ['name', 'year', 'session', 'credit_point', 'faculty', 'coordinator', 'description', 'location']
    success_url = reverse_lazy('lms_admin:unit')

    def get_initial(self):
        init = super().get_initial()

        init.update({
            'year': date.today().year
        })

        return init


class UnitEditView(UpdateView):
    template_name = 'LMS_Admin/unit_edit.html'
    model = Unit
    fields = ['name', 'year', 'session', 'credit_point', 'faculty', 'coordinator', 'description', 'location']
    success_url = reverse_lazy('lms_admin:unit')
