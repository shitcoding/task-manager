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
