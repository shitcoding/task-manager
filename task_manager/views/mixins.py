from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.deletion import ProtectedError
from django.utils.translation import gettext_lazy as _


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """LoginRequiredMixin showing error message when not logged in."""

    def handle_no_permission(self):
        """Show error message if user is not logged in."""
        messages.error(
            self.request,
            _("Please, log in to access this page"),
        )
        return super().handle_no_permission()


class SuccessOrProtectedErrorMessageMixin:
    """
    Mixin handling successful object deletion message and ProtectedError
    for generic.DeleteView.

    If object can be deleted, shows success message and redirects to success_url.
    If object is protected, shows protected_error_message and redirects
    to success_url.
    """

    success_message = "Object has been successfully deleted"
    protected_error_message = (
        "Cannot delete object referenced by a ForeignKey."
    )
    success_url = None

    def post(self, request, *args, **kwargs):
        """
        Delete the target object or show error message and redirect
        if object is referenced by a ForeignKey.
        """
        try:
            messages.success(
                self.request,
                self.success_message,
            )
            return self.delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                self.request,
                self.protected_error_message,
            )
            return self.success_url
