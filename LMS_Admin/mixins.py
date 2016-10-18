from LMS.mixins import ScopeRequiredMixin


class AdminMixin(ScopeRequiredMixin):
    def check_scope(self, user):
        return user.is_active and user.is_superuser
