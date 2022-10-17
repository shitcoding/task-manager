from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Field, Layout, Row, Submit
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from task_manager.models import SiteUser, Task


class SiteUserCreationForm(UserCreationForm):
    """User creation form."""

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ("username", "first_name", "last_name")


class SiteUserChangeForm(UserChangeForm):
    """User change form."""

    class Meta(UserChangeForm.Meta):
        model = SiteUser
        fields = ("username", "first_name", "last_name")


class TaskEditForm(forms.ModelForm):
    """Form for creation or edit of the task."""

    class Meta:
        model = Task
        fields = ("name", "description", "status", "performer", "label")

    def __init__(self, *args, **kwargs):
        """Set up form layout."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.layout = Layout(
            Field("name"),
            Field("description"),
            Row(
                Column("status", css_class="form-group"),
                Column("performer", css_class="form-group"),
            ),
            Column(
                "label",
                css_class="form-group",
                required=False,
            ),
            Submit("submit", _("Save"), css_class="btn btn-primary"),
            HTML(
                f"""
                <a class="btn btn-outline-primary" href="{reverse_lazy('tasks')}">
                    {_('Return to tasks list')}
                </a>
                """,
            ),
        )



class SelfTasksCheckbox(forms.Form):
    self_tasks = forms.BooleanField(
        label="Only own tasks",
        widget=forms.CheckboxInput,
        required=False,
    )
