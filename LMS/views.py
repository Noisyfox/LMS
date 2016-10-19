from account.views import LoginView as _LoginView
from django.views.generic import TemplateView

from LMS.timetable import generate_timetable


class LoginView(_LoginView):
    def get(self, *args, **kwargs):
        return super(_LoginView, self).get(*args, **kwargs)


class BaseTimetableView(TemplateView):
    def get_units(self):
        raise NotImplementedError

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['timetable'] = generate_timetable(self.get_units())

        return ctx
