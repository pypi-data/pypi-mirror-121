from django.core.management.base import BaseCommand
from esbuild import ESBUILD_VERSION, EsBuildLauncher
from esbuild.exceptions import EsbuildException


class Command(BaseCommand):
    help = "Installs Esbuild"

    def add_arguments(self, parser):
        parser.add_argument(
            "esbuild_version", nargs="?", type=str, default=ESBUILD_VERSION
        )

    def handle(self, *args, **options):
        version = options["esbuild_version"]
        esbuild = EsBuildLauncher()
        try:
            if esbuild.install(version):
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Successfully installed esbuild {version} to {esbuild.bin_path}"
                    )
                )
        except EsbuildException as err:
            self.stderr.write(self.style.ERROR(err))
