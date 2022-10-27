import django_filters
from django.utils.translation import gettext_lazy as _

from task_manager.forms import TaskFilterForm
from task_manager.models import Label, SiteUser, Status, Task


class TaskFilter(django_filters.FilterSet):
    """Task list filter."""

    status = django_filters.ModelChoiceFilter(
        label="",
        empty_label=_("Select status"),
        queryset=Status.objects.all(),
    )
    performer = django_filters.ModelChoiceFilter(
        label="",
        empty_label=_("Select performer"),
        queryset=SiteUser.objects.all(),
    )
    label = django_filters.ModelChoiceFilter(
        label="",
        empty_label=_("Select label"),
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
