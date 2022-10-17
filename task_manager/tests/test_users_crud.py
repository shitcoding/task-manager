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

    If no username is provided, unique uuid is used as a username.
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
def test_correct_user_creation(client, create_user, faker):
    """Test correct creation of a new user."""
    username = faker.user_name()
    first_name = faker.first_name()
    last_name = faker.last_name()

    test_user = create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
    assert SiteUser.objects.count() == 1
    assert test_user.username == username
    assert test_user.first_name == first_name
    assert test_user.last_name == last_name
    # Created user should be shown in users list
    client.force_login(test_user)
    response = client.get(reverse("users"))
    assert test_user.username in str(response.content)
    assert test_user.first_name in str(response.content)
    assert test_user.last_name in str(response.content)


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
    client, _ = auto_login_user()

    statuses_response = client.get(reverse("statuses"))
    assert statuses_response.status_code == 200

    labels_response = client.get(reverse("labels"))
    assert labels_response.status_code == 200

    tasks_response = client.get(reverse("tasks"))
    assert tasks_response.status_code == 200


@pytest.mark.django_db
def test_edit_other_user_permission_denied(client, create_user, faker):
    """
    Test an attempt of editing other user profile.

    Should redirect to user list page and show flash message with error.
    """
    test_user1 = create_user(username=faker.user_name())
    test_user2 = create_user(username=faker.user_name())
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


def test_update_own_user_account(client, auto_login_user, faker):
    """
    Test updating own user profile.

    Should change user profile data, redirect to user list page
    and show success flash message.
    """
    client, user = auto_login_user()
    # Assert that user can access own profile update page
    response = client.get(
        reverse("user_update", kwargs={"pk": user.pk}),
    )
    assert response.status_code == 200
    assert "User Update" in str(response.content)

    # Assert that user can change profile data
    new_username = faker.user_name()
    new_first_name = faker.first_name()
    new_last_name = faker.last_name()
    data = {
        "username": new_username,
        "first_name": new_first_name,
        "last_name": new_last_name,
    }
    response = client.post(
        reverse("user_update", kwargs={"pk": user.pk}),
        data,
    )
    # Should redirect to user list page
    assert response.status_code == 302
    assert response.url == reverse("users")
    # Should show success flash message after redirect
    redirect_response = client.get(response.url)
    assert "User info changed successfully" in str(
        redirect_response.content,
    )
    # User info should be changed successfully
    updated_user = SiteUser.objects.get(pk=user.pk)
    assert updated_user.username == new_username
    assert updated_user.first_name == new_first_name
    assert updated_user.last_name == new_last_name


def test_delete_own_user_account(client, auto_login_user):
    """
    Test deleting own user profile.

    Should delete user profile, redirect to user list page
    and show success flash message.
    """
    client, user = auto_login_user()
    # Assert that user can access own profile deletion page
    response = client.get(
        reverse("user_delete", kwargs={"pk": user.pk}),
    )
    assert response.status_code == 200
    assert "Delete account" in str(response.content)

    response = client.post(
        reverse("user_delete", kwargs={"pk": user.pk}),
    )
    # Should redirect to user list page
    assert response.status_code == 302
    assert response.url == reverse("users")
    # Should show success flash message after redirect
    redirect_response = client.get(response.url)
    assert "User deleted successfully" in str(
        redirect_response.content,
    )
    # User account should be deleted successfully
    with pytest.raises(SiteUser.DoesNotExist):
        updated_user = SiteUser.objects.get(pk=user.pk)
