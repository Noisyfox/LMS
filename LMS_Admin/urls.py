from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from LMS_Admin import views

app_name = 'lms_admin'

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='lms_admin:account_student'), name='home'),
    url(r'^account/', include([
        url(r'^student/', include([
            url(r'^$', views.AdminStudentListView.as_view(), name='account_student'),
            url(r'^new/$', views.StudentCreateView.as_view(), name='account_student_create'),
            url(r'^(?P<pk>[0-9]+)/$', views.StudentEditView.as_view(), name='account_student_edit'),
        ])),
        url(r'^teacher/$', TemplateView.as_view(template_name='LMS_Admin/account_student.html'),
            name='account_teacher'),
    ])),
]
