import datetime
from random import randrange

import pytest
from django.urls import reverse
from freezegun import freeze_time

from task_manager.models import Task
from task_manager.tests.fixtures import (
    auto_login_user,
    create_label,
    create_status,
    create_task,
    create_user,
    test_password,
)


@pytest.mark.django_db
def test_correct_task_creation(
    client,
    create_task,
    create_user,
    create_status,
    create_label,
    faker,
    auto_login_user,
):
    """Test correct creation of a new task."""
    name = faker.pystr(min_chars=10, max_chars=15)
    description = faker.paragraph(nb_sentences=5)
    creator = create_user()
    performer = create_user()
    created_on = faker.past_datetime(tzinfo=datetime.timezone.utc)
    status = create_status()
    # Creating random set of labels
    labels = []
    num_labels = randrange(1, 10)
    for _ in range(num_labels):
        labels.append(create_label())

    with freeze_time(created_on):  # setting mock datetime.now()
        task = Task.objects.create(
            name=name,
            description=description,
            creator=creator,
            performer=performer,
            status=status,
        )
    task.label.set(labels)

    assert Task.objects.count() == 1
    assert task.name == name
    assert task.description == description
    assert task.creator == creator
    assert task.performer == performer
    assert task.created_on == created_on
    assert task.status == status
    assert task.label.count() == num_labels
    assert list(task.label.all()) == labels

    # Created task should be shown on the tasks list page
    client, _ = auto_login_user()
    response = client.get(reverse("tasks"))
    page_content = str(response.content)
    assert task.name in page_content
    assert str(task.status) in page_content
    assert str(task.creator) in page_content
    assert str(task.performer) in page_content
