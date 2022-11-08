from crispy_forms.bootstrap import FormActions, InlineField, StrictButton
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML, Column, Field, Layout, Row, Submit
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.models import SiteUser, Task


class SiteUserCreationForm(UserCreationForm):
    """Signup form."""

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]

    def __init__(self, *args, **kwargs):
        """Set up form layout."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.form_class = "form-horizontal"
        self.helper.field_class = "col-lg-6 col-md-8"
        self.helper.form_show_labels = False
        self.helper.layout = Layout(
            Field("username", placeholder=_("Username")),
            Field("first_name", placeholder=_("First name")),
            Field("last_name", placeholder=_("Last name")),
            Field("password1", placeholder=_("Password")),
            Field("password2", placeholder=_("Password confirmation")),
            Submit(
                "submit",
                _("Sign up"),
                css_class="btn btn-primary mt-2",
            ),
        )


class SiteUserChangeForm(UserChangeForm):
    """User change form."""

    class Meta(UserChangeForm.Meta):
        model = SiteUser
        fields = ["username", "first_name", "last_name"]


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


class TaskFilterForm(forms.ModelForm):
    """Form for filtering tasks list."""

    class Meta:
        model = Task
        fields = [
            "status",
            "performer",
            "label",
        ]

    def __init__(self, *args, **kwargs):
        """Control form attributes and its layout."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-inline center"
        self.helper.form_tag = False
        self.helper.form_method = "GET"
        self.helper.layout = Layout(
            Row(
                InlineField(
                    "status",
                    css_class="mt-2 mr-2",
                ),
                InlineField(
                    "performer",
                    css_class="mt-2 mr-2",
                ),
                InlineField(
                    "label",
                    css_class="mt-2 mr-2",
                ),
                FormActions(
                    StrictButton(
                        _("Show"),
                        type="submit",
                        css_class="btn btn-primary mt-2 mr-2",
                    ),
                    HTML(
                        f"""
                    <a class="btn btn-outline-primary mt-2 mr-2" href="{reverse_lazy('tasks')}">
                        {_('Clear filters')}
                    </a>
                    """,
                    ),
                ),
                css_class="row col-12",
            ),
        )


class ToggleOnlyOwnTasks(forms.Form):
    """Checkbox for showing only own tasks in tasks list."""

    self_tasks = forms.BooleanField(
        label=_("Only own tasks"),
        widget=forms.CheckboxInput,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        """Control form attributes and its layout."""
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = "form-inline"
        self.helper.form_tag = False
        self.helper.form_method = "GET"
        self.helper.layout = Layout(
            Row(
                InlineField("self_tasks", css_class="form-group"),
                css_class="mb-2 pl-3",
            ),
        )
