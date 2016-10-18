from LMS.mixins import ScopeRequiredMixin


class TeacherMixin(ScopeRequiredMixin):
    def check_scope(self, user):
        return user.is_active and user.is_staff and not user.is_superuser
