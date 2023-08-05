# -*- coding: utf-8
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NobinobiStatsConfig(AppConfig):
    name = 'nobinobi_stats'
    verbose_name = _("Stats")

    def ready(self):
        try:
            import nobinobi_stats.signals  # noqa F401
        except ImportError:
            pass
