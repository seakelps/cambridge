from django.apps import AppConfig


class RankingConfig(AppConfig):
    name = "ranking"

    def ready(self):
        from . import signals  # noqa
