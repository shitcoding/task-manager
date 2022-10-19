import pytest
from django.urls import reverse

from task_manager.models import SiteUser
from task_manager.tests.fixtures import (
    auto_login_user,
    create_user,
    test_password,
)


@pytest.mark.django_db
def test_correct_user_creation(client, create_user, faker):
    """Test correct creation of a new user."""
    username = faker.user_name()
    first_name = faker.first_name()
    last_name = faker.last_name()

    user = create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
    )
    assert SiteUser.objects.count() == 1
    assert user.username == username
    assert user.first_name == first_name
    assert user.last_name == last_name
    # Created user should be shown in users list
    client.force_login(user)
    response = client.get(reverse("users"))
    assert user.username in str(response.content)
    assert user.first_name in str(response.content)
    assert user.last_name in str(response.content)


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


@pytest.mark.django_db
def test_edit_other_user_account_permission_denied(client, create_user, faker):
    """
    Test an attempt of editing other user profile.

    Should redirect to user list page and show flash message with error.
    """
    user1 = create_user(username=faker.user_name())
    user2 = create_user(username=faker.user_name())
    client.force_login(user1)
    response = client.get(
        reverse("user_update", kwargs={"pk": user2.pk}),
    )
    # Should redirect to user list page
    assert response.status_code == 302
    assert response.url == reverse("users")
    # Should show flash message with error after redirect
    redirect_response = client.get(response.url)
    assert "You have no permissions to change other user" in str(
        redirect_response.content,
    )


@pytest.mark.django_db
def test_edit_other_user_account_by_superuser(client, create_user, faker):
    """
    Test editing other user profile by superuser.

    Should change user profile data, redirect to user list page
    and show success flash message.
    """
    admin_user = create_user(
        username=faker.user_name(),
        is_staff=True,
        is_superuser=True,
    )
    user = create_user(username=faker.user_name())
    client.force_login(admin_user)

    # Assert that admin user can access other user's profile update page
    response = client.get(
        reverse("user_update", kwargs={"pk": user.pk}),
    )
    assert response.status_code == 200
    assert "User Update" in str(response.content)

    # Assert that admin user can change other user's profile data
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


@pytest.mark.django_db
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


@pytest.mark.django_db
def test_delete_other_user_permission_denied(client, create_user, faker):
    """
    Test an attempt of deleting other user's profile.

    Should redirect to user list page and show flash message with error.
    """
    user1 = create_user(username=faker.user_name())
    user2 = create_user(username=faker.user_name())
    client.force_login(user1)
    response = client.get(
        reverse("user_delete", kwargs={"pk": user2.pk}),
    )
    # Should redirect to user list page
    assert response.status_code == 302
    assert response.url == reverse("users")
    # Should show flash message with error after redirect
    redirect_response = client.get(response.url)
    assert "You have no permissions to change other user" in str(
        redirect_response.content,
    )


@pytest.mark.django_db
def test_delete_other_user_account_by_superuser(client, create_user, faker):
    """
    Test deleting other user's profile by superuser.

    Should delete target user profile, redirect to user list page
    and show success flash message.
    """
    admin_user = create_user(
        username=faker.user_name(),
        is_staff=True,
        is_superuser=True,
    )
    user = create_user(username=faker.user_name())
    client.force_login(admin_user)

    # Assert that admin user can access other user's profile deletion page
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
