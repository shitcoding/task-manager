from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from task_manager.forms import SitePasswordChangeForm, SiteUserChangeForm
from task_manager.models import SiteUser
from task_manager.views.mixins import (
    CustomLoginRequiredMixin,
    SuccessOrProtectedErrorMessageMixin,
)


class SiteUserListView(generic.ListView):
    """Site users list view."""

    template_name = "task_manager/user_list.html"
    context_object_name = "user_list"

    def get_queryset(self):
        """Return the list of all registered users."""
        return SiteUser.objects.order_by("-signup_date")


class SiteUserUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    generic.UpdateView,
):
    """User profile update page view."""

    model = SiteUser
    template_name = "registration/user_update.html"

    form_class = SiteUserChangeForm
    success_url = reverse_lazy("users")
    success_message = _("User info changed successfully")

    def test_func(self):
        """Check if user have permissions to update profile."""
        target_user = self.get_object()
        return (
            target_user == self.request.user or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        """Show error message if user has no permissions to update profile."""
        messages.error(
            self.request,
            _("You have no permissions to change other user"),
        )
        return redirect(reverse_lazy("users"))


class SiteUserDeleteView(
    CustomLoginRequiredMixin,
    SuccessOrProtectedErrorMessageMixin,
    UserPassesTestMixin,
    generic.DeleteView,
):
    """User deletion page view."""

    model = SiteUser
    template_name = "registration/user_delete.html"

    success_url = reverse_lazy("users")
    success_message = _("User deleted successfully")
    protected_error_message = _("Cannot delete the user assigned to task")

    def test_func(self):
        """Check if user have permissions to delete profile."""
        target_user = self.get_object()
        return (
            target_user == self.request.user or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        """Show error message if user has no permissions to delete profile."""
        messages.error(
            self.request,
            _("You have no permissions to change other user"),
        )
        return redirect(self.success_url)
