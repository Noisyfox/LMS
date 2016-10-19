from django.conf.urls import include, url
from django.views.generic import RedirectView

from LMS_Student import views

app_name = 'lms_stu'

urlpatterns = [
    url(r'^$', RedirectView.as_view(pattern_name='lms_stu:unit'), name='home'),
    url(r'^my_units/$', views.UnitListView.as_view(), name='unit'),
    url(r'^enroll/$', views.EnrollListView.as_view(), name='enroll'),
    url(r"^timetable/$", views.TimetableView.as_view(), name="timetable"),
    url(r'^unit/(?P<unit_id>[0-9]+)/', include([
        url(r'^info/$', views.UnitInfoView.as_view(), name='unit_info'),
        url(r'^material/', include([
            url(r'^$', views.MaterialListView.as_view(), name='material'),
            url(r'^(?P<material_id>[0-9]+)/$', views.MaterialDownloadView.as_view(), name='material_download'),
        ])),
        url(r'^assignment/', include([
            url(r'^$', views.AssignmentListView.as_view(), name='assignment'),
            url(r'^(?P<assignment_id>[0-9]+)/', include([
                url(r'^$', views.AssignmentFileListView.as_view(), name='assignment_detail'),
                url(r'^upload/$', views.AssignmentSubmitView.as_view(), name='assignment_submit'),
            ])),
        ])),
    ])),
]
