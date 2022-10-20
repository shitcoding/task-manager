import datetime

import pytest
from django.urls import reverse
from freezegun import freeze_time

from task_manager.models import Task
from task_manager.tests.fixtures import (
    auto_login_user,
    create_label,
    create_labels_set,
    create_status,
    create_task,
    create_user,
    test_password,
)


def test_task_creation(
    client,
    create_user,
    create_status,
    create_labels_set,
    faker,
    auto_login_user,
):
    """Test correct creation of a new task."""
    name = faker.pystr(min_chars=10, max_chars=15)
    description = faker.paragraph(nb_sentences=5)
    performer = create_user()
    created_on = faker.past_datetime(tzinfo=datetime.timezone.utc)
    status = create_status()
    labels = create_labels_set()

    data = {
        "name": name,
        "description": description,
        "status": status.pk,
        "performer": performer.pk,
        "label": [label.pk for label in labels],
    }

    client, user = auto_login_user()
    # mocking datetime.now() to test created_on with auto_now_add=True
    freezer = freeze_time(created_on)
    freezer.start()
    response = client.post(reverse("task_create"), data)
    freezer.stop()
    # Should redirect to tasks list page
    assert response.status_code == 302
    assert response.url == reverse("tasks")
    # Should show success flash message after redirect
    redirect_response = client.get(response.url)
    assert "Task created successfully" in str(
        redirect_response.content,
    )

    assert Task.objects.count() == 1
    task = Task.objects.all()[0]
    assert task.name == name
    assert task.description == description
    assert task.creator == user
    assert task.performer == performer
    assert task.created_on == created_on
    assert task.status == status
    assert task.label.count() == len(labels)
    assert list(task.label.all()) == labels

    # Created task should be shown on the tasks list page
    tasks_list_content = str(redirect_response.content)
    assert task.name in tasks_list_content
    assert str(task.status) in tasks_list_content
    assert str(task.creator) in tasks_list_content
    assert str(task.performer) in tasks_list_content


def test_task_update(
    client,
    create_task,
    create_user,
    create_status,
    create_labels_set,
    faker,
    auto_login_user,
):
    """
    Test updating task details.

    Should change task details, redirect to tasks list page
    and show success flash message.
    """
    task = create_task()

    new_name = faker.pystr(min_chars=10, max_chars=15)
    new_description = faker.paragraph(nb_sentences=5)
    new_performer = create_user()
    new_status = create_status()
    new_labels = create_labels_set()

    data = {
        "name": new_name,
        "description": new_description,
        "status": new_status.pk,
        "performer": new_performer.pk,
        "label": [label.pk for label in new_labels],
    }

    client, _ = auto_login_user()
    response = client.post(
        reverse("task_update", kwargs={"pk": task.pk}),
        data,
    )
    # Should redirect to tasks list page
    assert response.status_code == 302
    assert response.url == reverse("tasks")
    # Should show success flash message after redirect
    redirect_response = client.get(response.url)
    assert "Task updated successfully" in str(
        redirect_response.content,
    )
    # Task details should be changed successfully
    updated_task = Task.objects.get(pk=task.pk)
    assert updated_task.name == new_name
    assert updated_task.description == new_description
    assert updated_task.performer == new_performer
    assert updated_task.status == new_status
    assert updated_task.label.count() == len(new_labels)
    assert list(updated_task.label.all()) == new_labels
    # Created task should be shown on the tasks list page
    tasks_list_content = str(redirect_response.content)
    assert updated_task.name in tasks_list_content
    assert str(updated_task.status) in tasks_list_content
    assert str(updated_task.creator) in tasks_list_content
    assert str(updated_task.performer) in tasks_list_content
