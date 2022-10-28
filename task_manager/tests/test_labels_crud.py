import datetime

import pytest
from django.urls import reverse
from freezegun import freeze_time

from task_manager.models import Label
from task_manager.tests.fixtures import (
    auto_login_user,
    create_label,
    create_status,
    create_task,
    create_user,
    test_password,
    use_en_lang,
)


def test_label_creation(client, auto_login_user, faker):
    """Test correct creation of a new label."""
    client, _ = auto_login_user()
    name = faker.pystr(min_chars=10, max_chars=15)
    created_on = faker.past_datetime(tzinfo=datetime.timezone.utc)

    # mocking datetime.now() to test created_on with auto_now_add=True
    freezer = freeze_time(created_on)
    freezer.start()
    response = client.post(reverse("label_create"), {"name": name})
    freezer.stop()

    # Should redirect to labels list page
    assert response.status_code == 302
    assert response.url == reverse("labels")
    # Should show success flash message after redirect
    redirect_response = client.get(response.url)
    assert "Label created successfully" in str(
        redirect_response.content,
    )

    assert Label.objects.count() == 1
    label = Label.objects.all()[0]
    assert label.name == name
    assert label.created_on == created_on

    # Created label should be shown on the labels list page
    labels_list_content = str(redirect_response.content)
    assert label.name in labels_list_content
    assert (
        label.created_on.strftime("%d.%m.%Y %H:%M:%S") in labels_list_content
    )


def test_label_update(
    client,
    create_label,
    faker,
    auto_login_user,
):
    """
    Test updating label details.

    Should change label details, redirect to labels list page
    and show success flash message.
    """
    label = create_label()
    new_name = faker.pystr(min_chars=10, max_chars=15)

    client, _ = auto_login_user()
    response = client.post(
        reverse("label_update", kwargs={"pk": label.pk}),
        {"name": new_name},
    )
    # Should redirect to labels list page
    assert response.status_code == 302
    assert response.url == reverse("labels")
    # Should show success flash message after redirect
    redirect_response = client.get(response.url)
    assert "Label updated successfully" in str(
        redirect_response.content,
    )
    # Label details should be changed successfully
    updated_label = Label.objects.get(pk=label.pk)
    assert updated_label.name == new_name
    # Created label should be shown on the labels list page
    assert updated_label.name in str(redirect_response.content)


def test_delete_label(
    client,
    create_label,
    auto_login_user,
):
    """
    Test deleting a label with no tasks associated with it.

    Should delete a label, redirect to labels list page
    and show success flash message.
    """
    client, _ = auto_login_user()
    label = create_label()
    # Assert that user can access label deletion page
    response = client.get(
        reverse("label_delete", kwargs={"pk": label.pk}),
    )
    assert response.status_code == 200
    assert "Delete label" in str(response.content)

    response = client.post(
        reverse("label_delete", kwargs={"pk": label.pk}),
    )
    # Should redirect to labels list page
    assert response.status_code == 302
    assert response.url == reverse("labels")
    # Should show success flash message after redirect
    redirect_response = client.get(response.url)
    assert "Label deleted successfully" in str(
        redirect_response.content,
    )
    # Label should be deleted successfully
    with pytest.raises(Label.DoesNotExist):
        Label.objects.get(pk=label.pk)


def test_delete_label_with_associated_task(
    client,
    create_label,
    create_task,
    auto_login_user,
):
    """
    Test deleting a label with a task associated with it.

    Should redirect to labels list page and show flash message with error.
    """
    client, _ = auto_login_user()
    label = create_label()
    task = create_task()
    task.label.set([label])
    response = client.get(reverse("label_delete", kwargs={"pk": label.pk}))
    # Should redirect to labels list page
    assert response.status_code == 302
    assert response.url == reverse("labels")
    # Should show flash message with error after redirect
    redirect_response = client.get(response.url)
    assert "Can not delete the label associated with a task" in str(
        redirect_response.content,
    )
