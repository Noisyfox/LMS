class QueryMixin(object):
    def do_query(self, request, *args, **kwargs):
        raise NotImplemented

    def get(self, request, *args, **kwargs):
        self.do_query(request, *args, **kwargs)
        return super(QueryMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.do_query(request, *args, **kwargs)
        return super(QueryMixin, self).post(request, *args, **kwargs)
