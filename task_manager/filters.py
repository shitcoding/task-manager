import django_filters

from task_manager.forms import TaskFilterForm
from task_manager.models import Label, SiteUser, Status, Task


class TaskFilter(django_filters.FilterSet):
    """Task list filter."""

    status = django_filters.ModelChoiceFilter(
        label="",
        empty_label=("Select status"),
        queryset=Status.objects.all(),
    )
    performer = django_filters.ModelChoiceFilter(
        label="",
        empty_label=("Select performer"),
        queryset=SiteUser.objects.all(),
    )
    label = django_filters.ModelChoiceFilter(
        label="",
        empty_label=("Select label"),
        queryset=Label.objects.all(),
    )

    class Meta:
        model = Task
        form = TaskFilterForm

        fields = [
            "status",
            "performer",
            "label",
        ]
