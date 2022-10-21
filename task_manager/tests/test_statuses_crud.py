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
