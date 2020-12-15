from django.core.management import BaseCommand

from async_tasks.tasks import run_tasks


class Command(BaseCommand):
    help = 'Executes all publish tasks'

    def handle(self, *args, **options):
        self.stdout.write("Starting tasks...")
        run_tasks(self.stdout)
        self.stdout.write("Finished!")
