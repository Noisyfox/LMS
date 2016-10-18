from django.contrib.auth.mixins import AccessMixin
from django.urls import reverse_lazy


class QueryMixin(object):
    def do_query(self, request, *args, **kwargs):
        raise NotImplemented

    def get(self, request, *args, **kwargs):
        self.do_query(request, *args, **kwargs)
        return super(QueryMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.do_query(request, *args, **kwargs)
        return super(QueryMixin, self).post(request, *args, **kwargs)


class ScopeRequiredMixin(AccessMixin):
    login_url = reverse_lazy('account_login')

    def check_scope(self, user):
        raise NotImplementedError

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if not self.check_scope(request.user):
            # self.permission_denied_message = \
            #     "You are authenticated as %s, but are not authorized to access this page." \
            #     " Would you like to login to a different account?" % request.user.username
            return self.handle_no_permission()

        return super(ScopeRequiredMixin, self).dispatch(request, *args, **kwargs)
