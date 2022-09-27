import pytest

from task_manager.models import SiteUser


@pytest.mark.django_db
def test_user_create():
    """Test correct creation of a new user."""
    test_user = SiteUser.objects.create_user(
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
