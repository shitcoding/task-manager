from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from task_manager.models import Status
from task_manager.views.mixins import (
    CustomLoginRequiredMixin,
    SuccessOrProtectedErrorMessageMixin,
)


class StatusListView(CustomLoginRequiredMixin, generic.ListView):
    """Statuses list page view."""

    template_name = "task_manager/status_list.html"
    context_object_name = "status_list"

    def get_queryset(self):
        """Return the list of all statuses."""
        return Status.objects.order_by("-created_on")


class StatusCreateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    """Status creation page view."""

    template_name = "task_manager/status_create.html"
    model = Status
    fields = ["name"]
    success_url = reverse_lazy("statuses")
    success_message = _("Status created successfully")


class StatusUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Status update page view."""

    template_name = "task_manager/status_update.html"
    model = Status
    fields = ["name"]
    success_url = reverse_lazy("statuses")
    success_message = _("Status updated successfully")


class StatusDeleteView(
    CustomLoginRequiredMixin,
    SuccessOrProtectedErrorMessageMixin,
    generic.DeleteView,
):
    """Status deletion page view."""

    template_name = "task_manager/status_delete.html"
    model = Status
    success_url = reverse_lazy("statuses")
    success_message = _("Status deleted successfully")
    protected_error_message = _("Cannot delete the status assigned to task")
