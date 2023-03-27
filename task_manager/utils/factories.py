from datetime import timezone
from random import randrange

import factory
from factory.django import DjangoModelFactory
from override_autonow import override_autonow

from task_manager.models import Label, SiteUser, Status, Task


class OverrideAutoNowAddMixin:
    """
    Mixin for overriding Django's auto_now_add parameter
    when creating an object using factory.
    """

    @classmethod
    @override_autonow
    def _create(cls, model_class, *args, **kwargs):
        return super()._create(model_class, *args, **kwargs)


class SiteUserFactory(OverrideAutoNowAddMixin, DjangoModelFactory):
    class Meta:
        model = SiteUser
        django_get_or_create = ("username",)

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    signup_date = factory.Faker("date_time_this_year", tzinfo=timezone.utc)


class LabelFactory(OverrideAutoNowAddMixin, DjangoModelFactory):
    class Meta:
        model = Label
        django_get_or_create = ("name",)

    name = factory.Faker("text", max_nb_chars=20)
    created_on = factory.Faker("date_time_this_year", tzinfo=timezone.utc)


class StatusFactory(OverrideAutoNowAddMixin, DjangoModelFactory):
    class Meta:
        model = Status
        django_get_or_create = ("name",)

    name = factory.Faker("text", max_nb_chars=20)
    created_on = factory.Faker("date_time_this_year", tzinfo=timezone.utc)


class TaskFactory(OverrideAutoNowAddMixin, DjangoModelFactory):
    class Meta:
        model = Task

    name = factory.Faker("text", max_nb_chars=30)
    description = factory.Faker("text", max_nb_chars=1000)
    created_on = factory.Faker("date_time_this_year", tzinfo=timezone.utc)
    creator = factory.SubFactory(SiteUserFactory)
    performer = factory.SubFactory(SiteUserFactory)
    status = factory.SubFactory(StatusFactory)

    # Handle many-to-many relation of `label` field
    @factory.post_generation
    def label(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for label in extracted:
                self.label.add(label)
        else:
            for _ in range(randrange(1, 4)):
                self.label.add(LabelFactory())
