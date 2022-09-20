from django.db import models

from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext as _


class SiteUser(AbstractUser):
    """Model representing Task manager user account."""

    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    signup_date = models.DateTimeField("user signup date", auto_now_add=True)

    class Meta(object):
        verbose_name = _("User")
        verbose_name_plural = _("Users")

    def __str__(self):
        """Represent an instance as a string."""
        return self.username


class Label(models.Model):
    """Model representing a task label."""

    name = models.CharField(max_length=50)
    created_on = models.DateTimeField("label creation date", auto_now_add=True)

    def __str__(self):
        """Represent an instance as a string."""
        return self.name


class Status(models.Model):
    """Model representing a task status."""

    name = models.CharField(max_length=50)
    created_on = models.DateTimeField(
        "status creation date", auto_now_add=True
    )

    def __str__(self):
        """Represent an instance as a string."""
        return self.name


class Task(models.Model):
    """Model representing a task."""

    name = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(
        SiteUser, on_delete=models.CASCADE, related_name="creator"
    )
    performer = models.ForeignKey(
        SiteUser, on_delete=models.CASCADE, related_name="performer"
    )
    created_on = models.DateTimeField("task creation date", auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)

    def __str__(self):
        """Represent an instance as a string."""
        return self.name
