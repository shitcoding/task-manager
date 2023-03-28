from django.core.management.base import BaseCommand

from task_manager.utils.factories import TaskFactory


class Command(BaseCommand):
    help = "Creates dummy content (users, tasks, labels, statuses)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--num-tasks",
            default=10,
            type=int,
            required=False,
            help="Number of tasks to be created (default=10)",
        )

    def handle(self, *args, **options):
        # Create dummy tasks along with task creators, performers
        # statuses, labels
        num_tasks = options["num_tasks"]
        TaskFactory.create_batch(num_tasks)
        self.stdout.write(
            self.style.SUCCESS("Dummy content created successfully"),
        )
        self.stdout.write(f"{num_tasks} dummy tasks created")
