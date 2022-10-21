import datetime

import pytest
from django.urls import reverse
from freezegun import freeze_time

from task_manager.models import Status
from task_manager.tests.fixtures import (
    auto_login_user,
    create_status,
    create_user,
    test_password,
)


def test_status_creation(client, auto_login_user, faker):
    """Test correct creation of a new status."""
    client, user = auto_login_user()
    name = faker.pystr(min_chars=10, max_chars=15)
    created_on = faker.past_datetime(tzinfo=datetime.timezone.utc)

    # mocking datetime.now() to test created_on with auto_now_add=True
    freezer = freeze_time(created_on)
    freezer.start()
    response = client.post(reverse("status_create"), {"name": name})
    freezer.stop()

    # Should redirect to statuses list page
    assert response.status_code == 302
    assert response.url == reverse("statuses")
    # Should show success flash message after redirect
    redirect_response = client.get(response.url)
    assert "Status created successfully" in str(
        redirect_response.content,
    )

    assert Status.objects.count() == 1
    status = Status.objects.all()[0]
    assert status.name == name
    assert status.created_on == created_on

    # Created status should be shown on the statuses list page
    statuses_list_content = str(redirect_response.content)
    assert status.name in statuses_list_content
    assert (
        status.created_on.strftime("%d.%m.%Y %H:%M:%S")
        in statuses_list_content
    )


def test_status_update(
    client,
    create_status,
    faker,
    auto_login_user,
):
    """
    Test updating status details.

    Should change status details, redirect to statuses list page
    and show success flash message.
    """
    status = create_status()
    new_name = faker.pystr(min_chars=10, max_chars=15)

    client, _ = auto_login_user()
    response = client.post(
        reverse("status_update", kwargs={"pk": status.pk}),
        {"name": new_name},
    )
    # Should redirect to statuses list page
    assert response.status_code == 302
    assert response.url == reverse("statuses")
    # Should show success flash message after redirect
    redirect_response = client.get(response.url)
    assert "Status updated successfully" in str(
        redirect_response.content,
    )
    # Status details should be changed successfully
    updated_status = Status.objects.get(pk=status.pk)
    assert updated_status.name == new_name
    # Created status should be shown on the statuses list page
    assert updated_status.name in str(redirect_response.content)
