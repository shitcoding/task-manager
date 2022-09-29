import uuid

import pytest
from django.urls import reverse

from task_manager.models import SiteUser


@pytest.fixture
def test_password():
    return "Strong_test_password_1337"


@pytest.fixture
def create_user(db, django_user_model, test_password):
    """
    Fixture creating a new test user.
    If no username is provided, uuid is used as a username.
    """

    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = str(uuid.uuid4())
        return django_user_model.objects.create_user(**kwargs)

    return make_user


@pytest.fixture
def auto_login_user(db, client, create_user, test_password):
    """
    Fixture that automatically logs in a provided user.

    If no user is provided, a new test user is created and then is logged in.
    """

    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=test_password)
        return client, user

    return make_auto_login


@pytest.mark.django_db
def test_correct_user_creation(client, create_user):
    """Test correct creation of a new user."""
    test_user = create_user(
        username="username1",
        first_name="FirstName1",
        last_name="LastName1",
    )
    assert SiteUser.objects.count() == 1
    assert test_user.username == "username1"
    assert test_user.username != "username2"
    assert test_user.first_name == "FirstName1"
    assert test_user.first_name != "FirstName2"
    assert test_user.last_name == "LastName1"
    assert test_user.last_name != "LastName2"


@pytest.mark.django_db
def test_auth_urls_by_unauthorized_user(client):
    """
    Test accessing pages requiring authorization by unauthorized user.

    Should redirect to login page.
    After successful login should redirect to initially requested page.
    """
    login_url = reverse("login")

    statuses_url = reverse("statuses")
    statuses_response = client.get(statuses_url)
    assert statuses_response.status_code == 302
    assert statuses_response.url == f"{login_url}?next={statuses_url}"

    labels_url = reverse("labels")
    labels_response = client.get(labels_url)
    assert labels_response.status_code == 302
    assert labels_response.url == f"{login_url}?next={labels_url}"

    tasks_url = reverse("tasks")
    tasks_response = client.get(tasks_url)
    assert tasks_response.status_code == 302
    assert tasks_response.url == f"{login_url}?next={tasks_url}"


@pytest.mark.django_db
def test_auth_urls_by_authorized_user(client, auto_login_user):
    """
    Test accessing statuses, labels, tasks pages by authorized user.

    Should return status code 200.
    """
    client, user = auto_login_user()

    statuses_response = client.get(reverse("statuses"))
    assert statuses_response.status_code == 200

    labels_response = client.get(reverse("labels"))
    assert labels_response.status_code == 200

    tasks_response = client.get(reverse("tasks"))
    assert tasks_response.status_code == 200


@pytest.mark.django_db
def test_edit_other_user_permission_denied(client, create_user):
    """
    Test an attempt of editing other user profile.

    Should redirect to user list page and show flash message with error.
    """
    test_user1 = create_user(username="username1")
    test_user2 = create_user(username="username2")
    client.force_login(test_user1)
    response = client.get(
        reverse("user_update", kwargs={"pk": test_user2.pk}),
    )
    # Should redirect to user list page
    assert response.status_code == 302
    assert response.url == reverse("users")
    # Should show flash message with error after redirect
    redirect_response = client.get(response.url)
    assert "You have no permissions to change other user" in str(
        redirect_response.content,
    )
