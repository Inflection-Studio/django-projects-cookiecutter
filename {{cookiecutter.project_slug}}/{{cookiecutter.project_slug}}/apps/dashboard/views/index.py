from django.views.generic import TemplateView

from mixins.dashboard import AdminDashBoardMixin


# index page controller
class IndexTemplateView(AdminDashBoardMixin, TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
