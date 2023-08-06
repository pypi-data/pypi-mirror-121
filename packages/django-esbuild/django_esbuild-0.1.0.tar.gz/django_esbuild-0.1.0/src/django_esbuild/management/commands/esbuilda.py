from django.core.management import call_command
from django.core.management.base import BaseCommand

from ...conf import get_aliases


class Command(BaseCommand):
    help = "Runs esbuild alias command"

    def add_arguments(self, parser):
        parser.add_argument("alias", type=str)

    def handle(self, *args, **options):
        alias = options["alias"]
        try:
            cli_args = get_aliases()[options["alias"]]
            call_command("esbuild", cli_args)
        except KeyboardInterrupt:
            pass
        except KeyError:
            self.stderr.write(
                self.style.ERROR(
                    f"Can't find alias {alias} in ESBUILD_ALIASES dictionary in your settings."
                )
            )
