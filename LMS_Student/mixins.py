from LMS.mixins import ScopeRequiredMixin


class StudentMixin(ScopeRequiredMixin):
    def check_scope(self, user):
        return user.is_active and not user.is_staff and not user.is_superuser
