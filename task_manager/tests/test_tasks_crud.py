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
    use_en_lang,
)


def test_task_creation(
    client,
    create_user,
    create_status,
    create_labels_set,
    faker,
    auto_login_user,
    use_en_lang,
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
    assert task.created_on.strftime("%d.%m.%Y %H:%M:%S") in tasks_list_content


def test_task_details(
    client,
    create_task,
    auto_login_user,
    use_en_lang,
):
    """
    Test accessing task details page.

    Should return 200 status code, and task data should be present
    on the page.
    """
    client, user = auto_login_user()
    task = create_task()
    response = client.get(
        reverse("task_detail", kwargs={"pk": task.pk}),
    )
    # Assert that user can access task details page
    assert response.status_code == 200
    page_content = str(response.rendered_content)
    assert "Task details" in page_content
    # Assert that task data is present on task details page
    task_details = [
        task.name,
        task.description,
        task.creator,
        task.performer,
        task.status,
        task.created_on.strftime("%d.%m.%Y %H:%M:%S"),
    ]
    task_labels = list(task.label.all())
    for field in task_details + task_labels:
        assert str(field) in page_content


def test_task_update(
    client,
    create_task,
    create_user,
    create_status,
    create_labels_set,
    faker,
    auto_login_user,
    use_en_lang,
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


def test_delete_own_task(
    client,
    create_task,
    auto_login_user,
    use_en_lang,
):
    """
    Test deleting a task.

    Should delete a task, redirect to tasks list page
    and show success flash message.
    """
    client, user = auto_login_user()
    task = create_task(creator=user)
    # Assert that user can access own task deletion page
    response = client.get(
        reverse("task_delete", kwargs={"pk": task.pk}),
    )
    assert response.status_code == 200
    assert "Delete task" in str(response.content)

    response = client.post(
        reverse("task_delete", kwargs={"pk": task.pk}),
    )
    # Should redirect to tasks list page
    assert response.status_code == 302
    assert response.url == reverse("tasks")
    # Should show success flash message after redirect
    redirect_response = client.get(response.url)
    assert "Task deleted successfully" in str(
        redirect_response.content,
    )
    # Task should be deleted successfully
    with pytest.raises(Task.DoesNotExist):
        Task.objects.get(pk=task.pk)


def test_delete_other_users_task_permission_denied(
    client,
    create_task,
    create_user,
    auto_login_user,
    use_en_lang,
):
    """
    Test an attempt of deleting a task created by other user.

    Should redirect to tasks list page and show flash message with error.
    """
    client, user = auto_login_user()
    creator = create_user()
    task = create_task(creator=creator)
    response = client.get(
        reverse("task_delete", kwargs={"pk": task.pk}),
    )
    # Should redirect to tasks list page
    assert response.status_code == 302
    assert response.url == reverse("tasks")
    # Should show flash message with error after redirect
    redirect_response = client.get(response.url)
    assert "You cannot delete the task created by other user" in str(
        redirect_response.content,
    )
