from account.views import SignupView, LogoutView, ConfirmEmailView, ChangePasswordView, PasswordResetView, \
    PasswordResetTokenView, SettingsView, DeleteView
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from LMS import views

urlpatterns = [
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^admin/", include([
        url(r'^misc/', admin.site.urls),
        url(r'^', include('LMS_Admin.urls')),
    ])),
    url(r"^stu/", include("LMS_Student.urls")),
    url(r"^lec/", include("LMS_Teacher.urls")),
    url(r"^account/", include([
        url(r"^signup/$", SignupView.as_view(), name="account_signup"),
        url(r"^login/$", views.LoginView.as_view(), name="account_login"),
        url(r"^logout/$", LogoutView.as_view(), name="account_logout"),
        url(r"^confirm_email/(?P<key>\w+)/$", ConfirmEmailView.as_view(), name="account_confirm_email"),
        url(r"^password/$", ChangePasswordView.as_view(), name="account_password"),
        url(r"^password/reset/$", PasswordResetView.as_view(), name="account_password_reset"),
        url(r"^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$", PasswordResetTokenView.as_view(),
            name="account_password_reset_token"),
        url(r"^settings/$", SettingsView.as_view(), name="account_settings"),
        url(r"^delete/$", DeleteView.as_view(), name="account_delete"),
    ])),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
