from django.db import models


class User(models.Model):
    """Task manager user class."""
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    signup_date = models.DateTimeField('user signup date')

    def __str__(self):
        return self.username


class Label(models.Model):
    """Label class."""
    name = models.CharField(max_length=50)
    created_on = models.DateTimeField('label creation date')

    def __str__(self):
        return self.name


class Status(models.Model):
    """Task status class."""
    name = models.CharField(max_length=50)
    created_on = models.DateTimeField('status creation date')

    def __str__(self):
        return self.name


class Task(models.Model):
    """Task class."""
    name = models.CharField(max_length=200)
    description = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    performer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='performer')
    created_on = models.DateTimeField('task creation date')
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)

    def __str__(self):
        return self.name

