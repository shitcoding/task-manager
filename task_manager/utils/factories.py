from datetime import timezone

import factory
import faker.config
from factory.django import DjangoModelFactory
from override_autonow import override_autonow

from task_manager.models import Label, SiteUser, Status, Task

faker.config.DEFAULT_LOCALE = "en_US"


class SiteUserFactory(DjangoModelFactory):
    class Meta:
        model = SiteUser

    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    signup_date = factory.Faker("date_time_this_year", tzinfo=timezone.utc)

    @classmethod
    @override_autonow  # Overriding Django's auto_now_add parameter
    def _create(cls, model_class=SiteUser, *args, **kwargs):
        return super(SiteUserFactory, cls)._create(
            model_class,
            *args,
            **kwargs,
        )
