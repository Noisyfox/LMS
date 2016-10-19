from django.conf.urls import include, url

from LMS_Student import views

app_name = 'lms_stu'

urlpatterns = [
    url(r'^my_units/$', views.UnitListView.as_view(), name='unit'),
    url(r'^enroll/$', views.EnrollListView.as_view(), name='enroll'),
    url(r'^unit/(?P<unit_id>[0-9]+)/', include([
        url(r'^info/$', views.UnitInfoView.as_view(), name='unit_info'),
    ])),
]
