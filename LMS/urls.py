from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include([
        url(r'^misc/', admin.site.urls),
        url(r'^', include('LMS_Admin.urls')),
    ])),
    url(r"^stu/", include("LMS_Student.urls")),
    url(r"^lec/", include("LMS_Teacher.urls")),
    url(r"^account/", include("account.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
