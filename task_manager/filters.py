import django_filters

from task_manager.models import Task


class TaskFilter(django_filters.FilterSet):
    """Task list filter."""

    class Meta:
        model = Task
        fields = ["status", "performer", "label"]
