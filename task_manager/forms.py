from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from task_manager.models import SiteUser, Task


class UserCreationForm(UserCreationForm):
    """User creation form."""

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ("username", "first_name", "last_name")


class UserChangeForm(UserChangeForm):
    """User change form."""

    class Meta(UserChangeForm.Meta):
        model = SiteUser
        fields = ("username", "first_name", "last_name")


class TaskForm(forms.ModelForm):
    """Form for creation or edit of the task."""

    class Meta:
        model = Task
        fields = ("name", "description", "status", "performer", "label")


class SelfTasksCheckbox(forms.Form):
    self_tasks = forms.BooleanField(
        label="Only own tasks",
        widget=forms.CheckboxInput,
        required=False,
    )
