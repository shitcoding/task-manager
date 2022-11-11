from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from task_manager.forms import SitePasswordChangeForm, SiteUserCreationForm


class LoginView(SuccessMessageMixin, auth_views.LoginView):
    """Login page view."""

    next_page = reverse_lazy("index")
    success_message = _("You are logged in")


class SignupView(SuccessMessageMixin, generic.CreateView):
    """Signup page view."""

    form_class = SiteUserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    success_message = _("User created successfully")


class LogoutView(auth_views.LogoutView):
    """Logout page view."""

    def dispatch(self, request, *args, **kwargs):
        """Show flash message when authenticated user logs out."""
        if request.user.is_authenticated:
            messages.success(request, _("You are logged out"))
        return super().dispatch(request, *args, **kwargs)


class PasswordChangeView(SuccessMessageMixin, auth_views.PasswordChangeView):
    """User password change view."""

    form_class = SitePasswordChangeForm
    template_name = "registration/password_change.html"
    success_message = _("Password changed successfully")
    success_url = reverse_lazy("users")
