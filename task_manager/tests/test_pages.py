import pytest
from django.urls import reverse_lazy


def test_index_page(client):
    """Test loading index page."""
    response = client.get(reverse_lazy("index"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_list_page(client):
    """Test loading users list page."""
    response = client.get(reverse_lazy("users"))
    assert response.status_code == 200
