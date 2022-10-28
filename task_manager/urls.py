from django.contrib import admin
from django.urls import include, path

from task_manager import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.pages.IndexView.as_view(), name="index"),
    # Localization
    path("i18n/", include("django.conf.urls.i18n")),
    # Auth
    path("login/", views.auth.LoginView.as_view(), name="login"),
    path("logout/", views.auth.LogoutView.as_view(), name="logout"),
    path("users/create/", views.auth.SignupView.as_view(), name="signup"),
    # Users
    path("users/", views.users.SiteUserListView.as_view(), name="users"),
    path(
        "users/<int:pk>/update/",
        views.users.SiteUserUpdateView.as_view(),
        name="user_update",
    ),
    path(
        "users/<int:pk>/delete/",
        views.users.SiteUserDeleteView.as_view(),
        name="user_delete",
    ),
    # Tasks
    path("tasks/", views.tasks.TaskListView.as_view(), name="tasks"),
    path(
        "tasks/create/",
        views.tasks.TaskCreateView.as_view(),
        name="task_create",
    ),
    path(
        "tasks/<int:pk>/",
        views.tasks.TaskDetailView.as_view(),
        name="task_detail",
    ),
    path(
        "tasks/<int:pk>/update/",
        views.tasks.TaskUpdateView.as_view(),
        name="task_update",
    ),
    path(
        "tasks/<int:pk>/delete/",
        views.tasks.TaskDeleteView.as_view(),
        name="task_delete",
    ),
    # Statuses
    path(
        "statuses/",
        views.statuses.StatusListView.as_view(),
        name="statuses",
    ),
    path(
        "statuses/create/",
        views.statuses.StatusCreateView.as_view(),
        name="status_create",
    ),
    path(
        "statuses/<int:pk>/update/",
        views.statuses.StatusUpdateView.as_view(),
        name="status_update",
    ),
    path(
        "statuses/<int:pk>/delete/",
        views.statuses.StatusDeleteView.as_view(),
        name="status_delete",
    ),
    # Labels
    path("labels/", views.labels.LabelListView.as_view(), name="labels"),
    path(
        "labels/create/",
        views.labels.LabelCreateView.as_view(),
        name="label_create",
    ),
    path(
        "labels/<int:pk>/update/",
        views.labels.LabelUpdateView.as_view(),
        name="label_update",
    ),
    path(
        "labels/<int:pk>/delete/",
        views.labels.LabelDeleteView.as_view(),
        name="label_delete",
    ),
]
