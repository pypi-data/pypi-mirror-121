from django.conf import settings


def get_aliases():
    return getattr(settings, "ESBUILD_ALIASES", {})
