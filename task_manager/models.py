from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class SiteUser(AbstractUser):
    """Model representing Task manager user account."""

    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name=_("Username"),
    )
    first_name = models.CharField(
        max_length=100,
        verbose_name=_("First name"),
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name=_("Last name"),
    )
    signup_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Signup date"),
    )

    class Meta(object):
        verbose_name = _("User")

    def __str__(self):
        """Represent an instance as a string."""
        return self.username


class Label(models.Model):
    """Model representing a task label."""

    name = models.CharField(
        max_length=50,
        verbose_name=_("Name"),
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created on"),
    )

    class Meta(object):
        verbose_name = _("Label")

    def __str__(self):
        """Represent an instance as a string."""
        return self.name


class Status(models.Model):
    """Model representing a task status."""

    name = models.CharField(
        max_length=50,
        verbose_name=_("Name"),
    )

    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created on"),
    )

    class Meta(object):
        verbose_name = _("Status")

    def __str__(self):
        """Represent an instance as a string."""
        return self.name


class Task(models.Model):
    """Model representing a task."""

    name = models.CharField(
        max_length=200,
        verbose_name=_("Name"),
    )
    description = models.TextField(
        max_length=5000,
        verbose_name=_("Description"),
    )
    creator = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE,
        related_name="creator",
        verbose_name=_("Creator"),
    )
    performer = models.ForeignKey(
        SiteUser,
        on_delete=models.CASCADE,
        related_name="performer",
        verbose_name=_("Performer"),
    )
    created_on = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Created on"),
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.CASCADE,
        verbose_name=_("Status"),
    )
    label = models.ManyToManyField(
        Label,
        related_name="tasks",
        verbose_name=_("Label"),
    )

    class Meta(object):
        verbose_name = _("Task")

    def __str__(self):
        """Represent an instance as a string."""
        return self.name
