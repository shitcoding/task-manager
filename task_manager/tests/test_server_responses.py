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


@pytest.mark.parametrize(
    "need_pk, route",
    [
        (False, "tasks"),
        (False, "task_create"),
        (True, "task_detail"),
        (True, "task_update"),
        (True, "task_delete"),
    ],
)
def test_tasks_routes_by_authorized_user(
    need_pk, route, client, auto_login_user, create_task
):
    """
    Test accessing tasks routes by authorized user.

    Should return status code 200.
    """
    client, user = auto_login_user()

    test_task = create_task(creator=user)

    if need_pk:
        response = client.get(reverse(route, kwargs={"pk": test_task.pk}))
    else:
        response = client.get(reverse(route))
    assert response.status_code == 200


@pytest.mark.parametrize(
    "need_pk, route",
    [
        (False, "tasks"),
        (False, "task_create"),
        (True, "task_detail"),
        (True, "task_update"),
        (True, "task_delete"),
    ],
)
def test_tasks_routes_by_unauthorized_user(
    need_pk, route, client, create_task
):
    """
    Test accessing tasks routes by unauthorized user.

    Should redirect to login page.
    After successful login should redirect to initially requested page.
    """
    login_url = reverse("login")
    test_task = create_task()

    if need_pk:
        url = reverse(route, kwargs={"pk": test_task.pk})
    else:
        url = reverse(route)
    response = client.get(url)
    assert response.status_code == 302
    assert response.url == f"{login_url}?next={url}"
    assert response.status_code == 200
