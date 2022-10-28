from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from task_manager.models import Label
from task_manager.views.mixins import CustomLoginRequiredMixin


class LabelListView(CustomLoginRequiredMixin, generic.ListView):
    """Labels list page view."""

    template_name = "task_manager/label_list.html"
    context_object_name = "label_list"

    def get_queryset(self):
        """Return the list of all labels."""
        return Label.objects.order_by("-created_on")


class LabelCreateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    """Label creation page view."""

    template_name = "task_manager/label_create.html"
    model = Label
    fields = ["name"]
    success_url = reverse_lazy("labels")
    success_message = _("Label created successfully")


class LabelUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Label update page view."""

    template_name = "task_manager/label_update.html"
    model = Label
    fields = ["name"]
    success_url = reverse_lazy("labels")
    success_message = _("Label updated successfully")


class LabelDeleteView(
    CustomLoginRequiredMixin,
    UserPassesTestMixin,
    SuccessMessageMixin,
    generic.DeleteView,
):
    """Label deletion page view."""

    template_name = "task_manager/label_delete.html"
    model = Label
    success_url = reverse_lazy("labels")
    success_message = _("Label deleted successfully")

    def test_func(self):
        """Check if target label is associated with tasks."""
        return not self.get_object().tasks.all()

    def handle_no_permission(self):
        """
        Handle case when user has no permissions to delete the label.

        If user is not authenticated: redirect to login and show error message.
        If user is authenticated: show error message when deleting label
        associated with a task.
        """
        if not self.request.user.is_authenticated:
            return CustomLoginRequiredMixin.handle_no_permission(self)
        messages.error(
            self.request,
            _("Can not delete the label associated with a task"),
        )
        return redirect(reverse_lazy("labels"))
