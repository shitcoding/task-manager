from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import View, generic
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from task_manager.forms import UserChangeForm, UserCreationForm
from task_manager.models import Label, SiteUser, Status, Task


class CustomLoginRequiredMixin(LoginRequiredMixin):
    """LoginRequiredMixin with custom login page url."""

    login_url = "/login/"


class IndexView(generic.TemplateView):
    """Index page view."""

    template_name = "task_manager/index.html"


# Users
class LoginView(SuccessMessageMixin, auth_views.LoginView):
    """Login page view."""

    next_page = reverse_lazy("index")
    success_message = _("You are logged in")


class SignupView(SuccessMessageMixin, generic.CreateView):
    """Signup page view."""

    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")
    success_message = _("User created successfully")


class LogoutView(auth_views.LogoutView):
    """Logout page view."""

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, "You are logged out")
        return super().dispatch(request, *args, **kwargs)


class UserListView(generic.ListView):
    template_name = "task_manager/user_list.html"
    context_object_name = "user_list"

    def get_queryset(self):
        """Return the list of all registered users."""
        return SiteUser.objects.order_by("-signup_date")


class UserUpdateView(
    SuccessMessageMixin,
    CustomLoginRequiredMixin,
    UserPassesTestMixin,
    generic.UpdateView,
):
    """User profile update page view."""

    model = SiteUser
    template_name = "registration/user_update.html"

    form_class = UserChangeForm
    success_url = reverse_lazy("users")
    success_message = _("User info changed successfully")

    def get_context_data(self, **kwargs):
        """Add password change form to page context."""
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context["password_change_form"] = auth_views.PasswordChangeForm(
            user=self.request.user,
        )
        return context

    def test_func(self):
        """Check if user have permissions to update profile."""
        target_user = self.get_object()
        return (
            target_user == self.request.user or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        messages.error(
            self.request,
            "You have no permissions to change other user",
        )
        return redirect(reverse_lazy("users"))


class UserDeleteView(
    SuccessMessageMixin,
    CustomLoginRequiredMixin,
    UserPassesTestMixin,
    DeleteView,
):
    """User deletion page view."""

    model = SiteUser
    template_name = "registration/user_delete.html"

    success_url = reverse_lazy("users")
    success_message = _("User deleted successfully")

    def test_func(self):
        """Check if user have permissions to delete profile."""
        target_user = self.get_object()
        return (
            target_user == self.request.user or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        messages.error(
            self.request, "You have no permissions to change other user"
        )
        return redirect(reverse_lazy("users"))


# Tasks
class TaskListView(CustomLoginRequiredMixin, generic.ListView):
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"

    def get_queryset(self):
        """Return the list of all tasks."""
        return Task.objects.order_by("-created_on")


class TaskCreateView(CustomLoginRequiredMixin, View):
    """Task creation page view."""

    def get(self, request):
        return HttpResponse("You're at the task creation page")


class TaskDetailView(CustomLoginRequiredMixin, generic.DetailView):
    """Task detail page view."""

    model = Task
    template_name = "task_manager/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TaskUpdateView(CustomLoginRequiredMixin, View):
    """Task update page view."""

    def get(self, request, task_id):
        return HttpResponse(f"You're at task {task_id} update page")


class TaskDeleteView(CustomLoginRequiredMixin, View):
    """Task delete page view."""

    def get(self, request, task_id):
        return HttpResponse(f"You're at task {task_id} delete page")


# Statuses
class StatusListView(CustomLoginRequiredMixin, generic.ListView):
    template_name = "task_manager/status_list.html"
    context_object_name = "status_list"

    def get_queryset(self):
        """Return the list of all statuses."""
        return Status.objects.order_by("-created_on")


class StatusCreateView(CustomLoginRequiredMixin, CreateView):
    """Status creation page view."""

    template_name = "task_manager/status_create_form.html"
    model = Status
    fields = ["name"]
    success_url = reverse_lazy("statuses")


# class StatusUpdateView(CustomLoginRequiredMixin, View):
#     """Status update page view."""

#     def get(self, request, status_id):
#         return HttpResponse(f"You're at status {status_id} update page")


class StatusUpdateView(CustomLoginRequiredMixin, UpdateView):
    """Status update page view."""

    template_name = "task_manager/status_update_form.html"
    model = Status
    fields = ["name"]
    success_url = reverse_lazy("statuses")


class StatusDeleteView(CustomLoginRequiredMixin, View):
    """Status delete page view."""

    def get(self, request, status_id):
        return HttpResponse(f"You're at status {status_id} delete page")


# Labels
class LabelListView(CustomLoginRequiredMixin, generic.ListView):
    template_name = "task_manager/label_list.html"
    context_object_name = "label_list"

    def get_queryset(self):
        """Return the list of all labels."""
        return Label.objects.order_by("-created_on")


class LabelCreateView(CustomLoginRequiredMixin, View):
    """Label creation page view."""

    def get(self, request):
        return HttpResponse("You're at the label creation page")


class LabelUpdateView(CustomLoginRequiredMixin, View):
    """Label update page view."""

    def get(self, request, label_id):
        return HttpResponse(f"You're at label {label_id} update page")


class LabelDeleteView(CustomLoginRequiredMixin, View):
    """Label delete page view."""

    def get(self, request, label_id):
        return HttpResponse(f"You're at label {label_id} delete page")
