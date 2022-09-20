from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from django.views import generic, View

from .forms import UserCreationForm
from .models import SiteUser, Task, Label, Status


class IndexView(generic.TemplateView):
    """Index page view."""

    template_name = "task_manager/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        messages.info(self.request, "hello http://example.com")
        return context


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

    next_page = reverse_lazy("index")


class UserListView(generic.ListView):
    template_name = "task_manager/user_list.html"
    context_object_name = "user_list"

    def get_queryset(self):
        """Return the list of all registered users."""
        return SiteUser.objects.order_by("-signup_date")


class UserUpdateView(LoginRequiredMixin, View):
    """User update page view."""

    def get(self, request, user_id):
        return HttpResponse(f"You're at user {user_id} update page")


class UserDeleteView(LoginRequiredMixin, View):
    """User delete page view."""

    def get(self, request, user_id):
        return HttpResponse(f"You're at user {user_id} delete page")


# Tasks
class TaskListView(LoginRequiredMixin, generic.ListView):
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"

    def get_queryset(self):
        """Return the list of all tasks."""
        return Task.objects.order_by("-created_on")


class TaskCreateView(LoginRequiredMixin, View):
    """Task creation page view."""

    def get(self, request):
        return HttpResponse("You're at the task creation page")


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    """Task detail page view."""

    model = Task
    template_name = "task_manager/task_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TaskUpdateView(LoginRequiredMixin, View):
    """Task update page view."""

    def get(self, request, task_id):
        return HttpResponse(f"You're at task {task_id} update page")


class TaskDeleteView(LoginRequiredMixin, View):
    """Task delete page view."""

    def get(self, request, task_id):
        return HttpResponse(f"You're at task {task_id} delete page")


# Statuses
class StatusListView(LoginRequiredMixin, generic.ListView):
    template_name = "task_manager/status_list.html"
    context_object_name = "status_list"

    def get_queryset(self):
        """Return the list of all statuses."""
        return Status.objects.order_by("-created_on")


class StatusCreateView(LoginRequiredMixin, View):
    """Status creation page view."""

    def get(self, request):
        return HttpResponse("You're at the status creation page")


class StatusUpdateView(LoginRequiredMixin, View):
    """Status update page view."""

    def get(self, request, status_id):
        return HttpResponse(f"You're at status {status_id} update page")


class StatusDeleteView(LoginRequiredMixin, View):
    """Status delete page view."""

    def get(self, request, status_id):
        return HttpResponse(f"You're at status {status_id} delete page")


# Labels
class LabelListView(LoginRequiredMixin, generic.ListView):
    template_name = "task_manager/label_list.html"
    context_object_name = "label_list"

    def get_queryset(self):
        """Return the list of all labels."""
        return Label.objects.order_by("-created_on")


class LabelCreateView(LoginRequiredMixin, View):
    """Label creation page view."""

    def get(self, request):
        return HttpResponse("You're at the label creation page")


class LabelUpdateView(LoginRequiredMixin, View):
    """Label update page view."""

    def get(self, request, label_id):
        return HttpResponse(f"You're at label {label_id} update page")


class LabelDeleteView(LoginRequiredMixin, View):
    """Label delete page view."""

    def get(self, request, label_id):
        return HttpResponse(f"You're at label {label_id} delete page")
