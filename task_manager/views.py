from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from django.views import generic

from .models import User, Task, Label, Status


def index(request):
    return render(request, "task_manager/index.html")


# Users
def login(request):
    return HttpResponse("You're at login page")


def signup(request):
    return HttpResponse("You're at signup page")


def logout(request):
    return HttpResponse("You're at logout page")


class UserListView(generic.ListView):
    template_name = "task_manager/users.html"
    context_object_name = "users_list"

    def get_queryset(self):
        """Return the list of all registered users."""
        return User.objects.order_by("-signup_date")


def user_update(request, user_id):
    return HttpResponse(f"You're at user {user_id} update page")


def user_delete(request, user_id):
    return HttpResponse(f"You're at user {user_id} delete page")


# Tasks
def tasks(request):
    return HttpResponse("You're at the tasks list page")


def task_create(request):
    return HttpResponse("You're at the task creation page")


def task_detail(request, task_id):
    return HttpResponse(f"You're at task {task_id} details page")


def task_update(request, task_id):
    return HttpResponse(f"You're at task {task_id} update page")


def task_delete(request, task_id):
    return HttpResponse(f"You're at task {task_id} delete page")


# Statuses
def statuses(request):
    return HttpResponse("You're at the statuses list page")


def status_create(request):
    return HttpResponse("You're at the status creation page")


def status_update(request, status_id):
    return HttpResponse(f"You're at status {status_id} update page")


def status_delete(request, status_id):
    return HttpResponse(f"You're at status {status_id} delete page")


# Labels
def labels(request):
    return HttpResponse("You're at the labels list page")


def label_create(request):
    return HttpResponse("You're at the label creation page")


def label_update(request, label_id):
    return HttpResponse(f"You're at label {label_id} update page")


def label_delete(request, label_id):
    return HttpResponse(f"You're at label {label_id} delete page")
