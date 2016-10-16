from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.datetime_safe import date
from django.views.generic import FormView
from django.views.generic import ListView

from LMS.models import Student
from LMS_Admin.forms import StudentEditForm
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
