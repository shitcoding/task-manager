from django.views import generic


class IndexView(generic.TemplateView):
    """Index page view."""

    template_name = "task_manager/index.html"
