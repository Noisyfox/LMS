from django.conf.urls import include, url

from LMS_Teacher import views

app_name = 'lms_tec'

urlpatterns = [
    url(r'^my_units/$', views.UnitListView.as_view(), name='unit'),
]
