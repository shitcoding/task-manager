from random import randrange

import pytest

from task_manager.models import Label, Status, Task


@pytest.fixture(autouse=True)
def use_en_lang(settings):
    settings.LANGUAGE_CODE = "en"


@pytest.fixture
def test_password():
    return "Strong_test_password_1337"


@pytest.fixture
def create_user(db, django_user_model, test_password, faker):
    """
    Fixture creating a new test user.

    If no username is provided, unique uuid is used as a username.
    """

    def make_user(**kwargs):
        kwargs["password"] = test_password
        if "username" not in kwargs:
            kwargs["username"] = faker.user_name()
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


@pytest.fixture
def create_status(db, faker):
    """
    Fixture creating a test status.

    If no name or creation date is provided,
    random one is created and assigned.
    """

    def make_status(**kwargs):
        if "name" not in kwargs:
            kwargs["name"] = faker.pystr(min_chars=10, max_chars=15)
        if "created_on" not in kwargs:
            kwargs["created_on"] = faker.past_datetime()
        return Status.objects.create(**kwargs)

    return make_status


@pytest.fixture
def create_label(db, faker):
    """
    Fixture creating a test label.

    If no name or creation date is provided,
    random one is created and assigned.
    """

    def make_label(**kwargs):
        if "name" not in kwargs:
            kwargs["name"] = faker.pystr(min_chars=10, max_chars=15)
        if "created_on" not in kwargs:
            kwargs["created_on"] = faker.past_datetime()
        return Label.objects.create(**kwargs)

    return make_label


@pytest.fixture
def create_labels_set(db, create_label):
    """
    Fixture creating a random set of labels.

    Returns list of label objects.
    """

    def make_labels_set(min=1, max=10):
        labels = []
        for _ in range(randrange(min, max)):
            labels.append(create_label())
        return labels

    return make_labels_set


@pytest.fixture
def create_task(db, faker, create_user, create_status, create_label):
    """
    Fixture creating a test task.

    If no name/description/creator/performer is provided,
    random one is created and assigned.
    """

    def make_task(**kwargs):
        if "name" not in kwargs:
            kwargs["name"] = faker.pystr(min_chars=10, max_chars=15)
        if "description" not in kwargs:
            kwargs["description"] = faker.paragraph(nb_sentences=5)
        if "creator" not in kwargs:
            kwargs["creator"] = create_user()
        if "performer" not in kwargs:
            kwargs["performer"] = create_user()
        if "created_on" not in kwargs:
            kwargs["created_on"] = faker.past_datetime()
        if "status" not in kwargs:
            kwargs["status"] = create_status()
        # Remove label from kwargs in order to assign it via
        # many-to-many manager with Task.label.set()
        label = kwargs.pop("label", create_label())

        task = Task.objects.create(**kwargs)
        if isinstance(label, list):
            task.label.set(label)
        elif isinstance(label, Label):
            task.label.set([label])
        return task

    return make_task


@pytest.fixture
def create_tasks_set(db, create_task):
    """
    Fixture creating a random set of tasks.

    If num_tasks argument is provided, number of created tasks
    equals num_tasks. Otherwise, number of created tasks is
    random beetween min and max.
    Returns list of created Task objects.
    """

    def make_tasks_set(num_tasks=None, min=1, max=10, **kwargs):
        tasks = []
        if not num_tasks:
            num_tasks = randrange(min, max)
        for _ in range(num_tasks):
            tasks.append(create_task(**kwargs))
        return tasks

    return make_tasks_set
