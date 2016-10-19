from django.conf.urls import include, url

from LMS_Teacher import views

app_name = 'lms_tec'

urlpatterns = [
    url(r'^my_units/$', views.UnitListView.as_view(), name='unit'),
    url(r"^timetable/$", views.TimetableView.as_view(), name="timetable"),
    url(r'^unit/(?P<unit_id>[0-9]+)/', include([
        url(r'^info/$', views.UnitInfoView.as_view(), name='unit_info'),
        url(r'^material/', include([
            url(r'^$', views.MaterialListView.as_view(), name='material'),
            url(r'^upload/$', views.MaterialCreateView.as_view(), name='material_upload'),
            url(r'^(?P<material_id>[0-9]+)/', include([
                url(r'^$', views.MaterialEditView.as_view(), name='material_edit'),
                url(r'^delete/$', views.MaterialDeleteView.as_view(), name='material_delete'),
            ])),
        ])),
        url(r'^assignment/', include([
            url(r'^$', views.AssignmentListView.as_view(), name='assignment'),
            url(r'^create/$', views.AssignmentCreateView.as_view(), name='assignment_create'),
            url(r'^(?P<assignment_id>[0-9]+)/', include([
                url(r'^$', views.AssignmentFileListView.as_view(), name='assignment_file'),
                url(r'^edit/$', views.AssignmentEditView.as_view(), name='assignment_edit'),
                url(r'^delete/$', views.AssignmentDeleteView.as_view(), name='assignment_delete'),
            ])),
        ])),
    ]))
]
