from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import SiteUser, Task, Status, Label


class SiteUserAdmin(UserAdmin):
    """Site user representation."""

    model = SiteUser
    add_form = UserCreationForm
    form = UserChangeForm


admin.site.register(SiteUser, SiteUserAdmin)
admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Label)
