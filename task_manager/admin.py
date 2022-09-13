from django.contrib import admin

from .models import User, Task, Status, Label


admin.site.register(Task)
admin.site.register(Status)
admin.site.register(Label)
