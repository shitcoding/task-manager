from django.contrib.auth import forms
from django.forms import ModelForm

from task_manager.models import SiteUser, Task


class UserCreationForm(forms.UserCreationForm):
    """User creation form."""

    class Meta(forms.UserCreationForm.Meta):
        model = SiteUser
        fields = ("username", "first_name", "last_name")


class UserChangeForm(forms.UserChangeForm):
    """User change form."""

    class Meta(forms.UserChangeForm.Meta):
        model = SiteUser
        fields = ("username", "first_name", "last_name")


class TaskCreationForm(ModelForm):
    """Task creation form."""

    class Meta:
        model = Task
        fields = ("name", "description", "status", "performer", "label")
