from django.conf.urls import include, url
from django.views.generic import RedirectView

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
        url(r'^teacher/', include([
            url(r'^$', views.AdminTeacherListView.as_view(), name='account_teacher'),
            url(r'^new/$', views.TeacherCreateView.as_view(), name='account_teacher_create'),
            url(r'^(?P<pk>[0-9]+)/$', views.TeacherEditView.as_view(), name='account_teacher_edit'),
        ])),
        url(r'^unit/', include([
            url(r'^$', views.AdminUnitListView.as_view(), name='unit'),
            url(r'^new/$', views.UnitCreateView.as_view(), name='unit_create'),
            url(r'^(?P<unit_id>[0-9]+)/', include([
                url(r'^$', views.UnitEditView.as_view(), name='unit_edit'),
                url(r'^staff/', include([
                    url(r'^$', views.StaffListView.as_view(), name='unit_staff'),
                    url(r'^add/$', views.StaffAddView.as_view(), name='unit_staff_add'),
                    url(r'^(?P<alloc_id>[0-9]+)/', include([
                        url(r'^$', views.StaffEditView.as_view(), name='unit_staff_edit'),
                        url(r'^delete/$', views.StaffDeleteView.as_view(), name='unit_staff_delete'),
                    ])),
                ])),
            ])),
        ])),
    ])),
]
