from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views import generic

from task_manager.filters import TaskFilter
from task_manager.forms import TaskEditForm, ToggleOnlyOwnTasks
from task_manager.models import Task
from task_manager.views.mixins import CustomLoginRequiredMixin


class TaskListView(CustomLoginRequiredMixin, generic.ListView):
    """Tasks list page view."""

    template_name = "task_manager/task_list.html"

    def get_queryset(self, self_tasks=False):
        """Return the list of all tasks."""
        if self_tasks:
            queryset = Task.objects.filter(creator=self.request.user)
        else:
            queryset = Task.objects.order_by("-created_on")
        task_filter = TaskFilter(self.request.GET, queryset)
        return task_filter.qs

    def get_context_data(self, **kwargs):
        """Get context data of task filter view."""
        context = super().get_context_data(**kwargs)
        toggle_self_tasks = ToggleOnlyOwnTasks(self.request.GET)
        context["toggle_self_tasks"] = toggle_self_tasks
        self_tasks = toggle_self_tasks.data.get("self_tasks", None) == "on"
        queryset = self.get_queryset(self_tasks)
        task_filter = TaskFilter(self.request.GET, queryset)
        context["task_filter"] = task_filter
        return context


class TaskCreateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.CreateView,
):
    """Task creation page view."""

    model = Task
    form_class = TaskEditForm
    template_name = "task_manager/task_create.html"
    success_url = reverse_lazy("tasks")
    success_message = _("Task created successfully")

    def form_valid(self, form):
        """Set current user as task creator."""
        task = form.save(commit=False)
        task.creator = self.request.user
        task.save()
        return super().form_valid(form)


class TaskDetailView(CustomLoginRequiredMixin, generic.DetailView):
    """Task detail page view."""

    model = Task
    template_name = "task_manager/task_detail.html"


class TaskUpdateView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    generic.UpdateView,
):
    """Task update page view."""

    model = Task
    form_class = TaskEditForm
    template_name = "task_manager/task_update.html"
    success_url = reverse_lazy("tasks")
    success_message = _("Task updated successfully")


class TaskDeleteView(
    CustomLoginRequiredMixin,
    SuccessMessageMixin,
    UserPassesTestMixin,
    generic.DeleteView,
):
    """Task delete page view."""

    model = Task
    template_name = "task_manager/task_delete.html"

    success_url = reverse_lazy("tasks")
    success_message = _("Task deleted successfully")

    def test_func(self):
        """Check if user have permissions to delete the task."""
        task_creator = self.get_object().creator
        return (
            task_creator == self.request.user or self.request.user.is_superuser
        )

    def handle_no_permission(self):
        """
        Handle case when user has no permissions to delete the task.

        If user is not authenticated: redirect to login and show error message.
        If user is authenticated: show error message when deleting task created
        by other user.
        """
        if not self.request.user.is_authenticated:
            return CustomLoginRequiredMixin.handle_no_permission(self)
        messages.error(
            self.request,
            _("You cannot delete the task created by other user"),
        )
        return redirect(reverse_lazy("tasks"))
