import pytest
from django.urls import reverse

from task_manager.models import Task
from task_manager.tests.fixtures import (
    auto_login_user,
    create_label,
    create_labels_set,
    create_status,
    create_task,
    create_tasks_set,
    create_user,
    test_password,
    use_en_lang,
)


def test_task_filtering_by_status(
    client,
    create_tasks_set,
    create_status,
    auto_login_user,
):
    """
    Test filtering tasks list by status.

    Should return tasks set with specified status.
    """
    target_status = create_status()
    target_tasks = create_tasks_set(num_tasks=10, status=target_status)
    other_tasks = create_tasks_set(min=10, max=20)

    client, user = auto_login_user()
    response = client.get(
        reverse("tasks"),
        {"status": target_status.pk},
    )
    filtered_tasks = response.context_data["task_filter"].queryset
    # Filtered tasks set should be identical to initial target_tasks set
    assert set(filtered_tasks) == set(target_tasks)
    # Each filtered task's status should be target_status
    for task in filtered_tasks:
        assert task.status == target_status


def test_task_filtering_by_label(
    client,
    create_tasks_set,
    create_labels_set,
    auto_login_user,
):
    """
    Test filtering tasks list by labels.

    Should return tasks set with specified labels.
    """
    target_labels = create_labels_set()
    target_tasks = create_tasks_set(num_tasks=10, label=target_labels)
    other_tasks = create_tasks_set(min=10, max=20)

    client, user = auto_login_user()
    response = client.get(
        reverse("tasks"),
        {"label": [label.pk for label in target_labels]},
    )
    filtered_tasks = response.context_data["task_filter"].queryset
    # Filtered tasks set should be identical to initial target_tasks set
    assert set(filtered_tasks) == set(target_tasks)
    # Each filtered task's labels should be target_labels
    for task in filtered_tasks:
        assert set(task.label.all()) == set(target_labels)


def test_task_filtering_by_performer(
    client,
    create_tasks_set,
    create_user,
    auto_login_user,
):
    """
    Test filtering tasks list by performer.

    Should return tasks set with specified performer.
    """
    target_performer = create_user()
    target_tasks = create_tasks_set(num_tasks=10, performer=target_performer)
    create_tasks_set(min=10, max=20)

    client, user = auto_login_user()
    response = client.get(
        reverse("tasks"),
        {"performer": target_performer.pk},
    )
    filtered_tasks = response.context_data["task_filter"].queryset
    # Filtered tasks set should be identical to initial target_tasks set
    assert set(filtered_tasks) == set(target_tasks)
    # Each filtered task's performer should be target_performer
    for task in filtered_tasks:
        assert task.performer == target_performer


def test_task_filtering_own_tasks(
    client,
    create_tasks_set,
    create_user,
    auto_login_user,
):
    """
    Test filtering only own tasks.

    Should return only the tasks created by user.
    """
    client, target_user = auto_login_user()
    target_tasks = create_tasks_set(num_tasks=10, creator=target_user)
    create_tasks_set(min=10, max=20)

    response = client.get(
        reverse("tasks"),
        {"self_tasks": "on"},
    )
    filtered_tasks = response.context_data["task_filter"].queryset
    # Filtered tasks set should be identical to initial target_tasks set
    assert set(filtered_tasks) == set(target_tasks)
    # Each filtered task's creator should be target_user
    for task in filtered_tasks:
        assert task.creator == target_user
