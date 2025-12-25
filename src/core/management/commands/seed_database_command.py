from django.core.management import call_command, CommandError

from database.seeders.group_seeder import GroupSeeder
from database.seeders.media_seeder import MediaSeeder
from database.seeders.user_seeder import UserSeeder
from chatapp import settings
from src.core.management.commands.base_command import BaseCommand


class Command(BaseCommand):
    help = 'Seeds the database'

    def add_arguments(self, parser):
        parser.add_argument("env", type=str, help="local or prod")
        parser.add_argument("--truncate", action="store_true", default=False)

    def handle(self, *args, **options):
        env = options["env"]

        if env == 'prod':
            self.write('Seeding groups')
            GroupSeeder.seed()
            return

        if settings.APP_ENV != 'local' and env != 'local':
            raise CommandError('You are not in local env')

        should_truncate = options["truncate"]

        if should_truncate:
            call_command("flush", interactive=False)

        call_command("makemigrations", interactive=False)
        call_command("migrate")

        self.write('Seeding groups')
        GroupSeeder.seed()

        self.write('Seeding users')
        UserSeeder.seed()

        self.write('Seeding media')
        MediaSeeder.seed()

        self.stdout.write(self.style.SUCCESS('Done'))

    def write(self, string: str) -> None:
        self.stdout.write(self.style.SUCCESS(string))
