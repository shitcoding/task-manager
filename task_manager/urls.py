from django.contrib import admin
from django.urls import path, include

from . import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.IndexView.as_view(), name="index"),
    # Auth
    path("login/", views.LoginView.as_view(), name="login"),
    path("accounts/", include("django.contrib.auth.urls")),  # login test
    path("logout/", views.LogoutView.as_view(), name="logout"),
    # Users
    path("users/create/", views.SignupView.as_view(), name="signup"),
    path("users/", views.UserListView.as_view(), name="users"),
    path(
        "users/<int:user_id>/update/",
        views.UserUpdateView.as_view(),
        name="user_update",
    ),
    path(
        "users/<int:user_id>/delete/",
        views.UserDeleteView.as_view(),
        name="user_delete",
    ),
    # Tasks
    path("tasks/", views.TaskListView.as_view(), name="tasks"),
    path("tasks/create/", views.TaskCreateView.as_view(), name="task_create"),
    path(
        "tasks/<int:pk>/",
        views.TaskDetailView.as_view(),
        name="task_detail",
    ),
    path(
        "tasks/<int:task_id>/update/",
        views.TaskUpdateView.as_view(),
        name="task_update",
    ),
    path(
        "tasks/<int:task_id>/delete/",
        views.TaskDeleteView.as_view(),
        name="task_delete",
    ),
    # Statuses
    path("statuses/", views.StatusListView.as_view(), name="statuses"),
    path(
        "statuses/create/",
        views.StatusCreateView.as_view(),
        name="status_create",
    ),
    path(
        "statuses/<int:status_id>/update/",
        views.StatusUpdateView.as_view(),
        name="status_update",
    ),
    path(
        "statuses/<int:status_id>/delete/",
        views.StatusDeleteView.as_view(),
        name="status_delete",
    ),
    # Labels
    path("labels/", views.LabelListView.as_view(), name="labels"),
    path(
        "labels/create/", views.LabelCreateView.as_view(), name="label_create"
    ),
    path(
        "labels/<int:label_id>/update/",
        views.LabelUpdateView.as_view(),
        name="label_update",
    ),
    path(
        "labels/<int:label_id>/delete/",
        views.LabelDeleteView.as_view(),
        name="label_delete",
    ),
]
