from django.contrib.auth import forms

from task_manager.models import SiteUser


class UserCreationForm(forms.UserCreationForm):
    """Task manager user creation form."""

    class Meta(forms.UserCreationForm.Meta):
        model = SiteUser
        fields = ("username", "first_name", "last_name")


class UserChangeForm(forms.UserChangeForm):
    """Task manager user change form."""

    class Meta(forms.UserChangeForm.Meta):
        model = SiteUser
        fields = ("username", "first_name", "last_name")
