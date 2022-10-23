from django.db import models
from django.utils.translation import gettext_lazy as _


class Gender(models.IntegerChoices):
    MALE = 1, _('MALE')
    FEMALE = 2, _('FEMALE')
    UNKNOWN = 0, _('UNKNOWN')


class MatchStatus(models.IntegerChoices):
    RUNNING = 0, _("Running")
    FINISHED = 1, _("Finished")
    ABANDONED = 2, _("Abandoned")
    INCOMPLETE = 3, _("Incomplete")
