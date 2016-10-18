from account.views import LoginView as _LoginView
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
from LMS.models import Student, Teacher, Unit, UnitAllocation
from LMS_Admin.forms import StudentEditForm, TeacherEditForm
from LMS_Admin.mixins import AdminMixin
from LMS_Admin.models import UidGen


class LoginView(_LoginView):
    def get(self, *args, **kwargs):
        return super(_LoginView, self).get(*args, **kwargs)
