import pytest
from django.urls import reverse

from task_manager.tests.fixtures import (
    auto_login_user,
    create_label,
    create_status,
    create_task,
    create_user,
    test_password,
)


def test_index_page(client):
    """Test loading index page."""
    response = client.get(reverse("index"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_list_page(client):
    """Test loading users list page."""
    response = client.get(reverse("users"))
    assert response.status_code == 200
    assert response.status_code == 200
