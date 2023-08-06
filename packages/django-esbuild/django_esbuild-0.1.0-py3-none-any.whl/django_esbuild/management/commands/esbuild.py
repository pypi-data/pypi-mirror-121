import os
import sys
from subprocess import CompletedProcess

from django.core.management.base import BaseCommand, CommandError, SystemCheckError
from esbuild import EsBuildLauncher


class Command(BaseCommand):
    help = "Runs esbuild"

    def add_arguments(self, parser):
        parser.add_argument("esbuild_args", nargs="+", type=str)

    def handle_plain(self, args, **options):
        env = os.environ.copy()
        esbuild = EsBuildLauncher(auto_install=True)
        return esbuild.run(args, env=env, live_output=True)

    def execute(self, args=None, **options):
        esbuild_args = args or options.get("esbuild_args")[0]
        output = self.handle_plain(esbuild_args, **options)
        if output and not isinstance(output, CompletedProcess):
            self.stdout.write(output)
        return output

    def run_from_argv(self, argv):
        esbuild_args = argv[2:]
        try:
            self.execute(esbuild_args, **dict())
        except KeyboardInterrupt:
            pass
        except CommandError as e:
            # SystemCheckError takes care of its own formatting.
            if isinstance(e, SystemCheckError):
                self.stderr.write(str(e), lambda x: x)
            else:
                self.stderr.write("%s: %s" % (e.__class__.__name__, e))
            sys.exit(e.returncode)
