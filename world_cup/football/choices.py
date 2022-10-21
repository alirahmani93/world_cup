from django.db import models
from django.utils.translation import gettext_lazy as _


class Continent(models.IntegerChoices):
    ASIA = 0, _('Asia')
    EUROPE = 1, _('Europe')
    AFRICA = 2, _('Africa')
    NORTH_AMERICA = 3, _('North America')
    SOUTH_AMERICA = 4, _('South America')
    Oceania = 5, _('South Oceania')


class WorldCupGroup(models.IntegerChoices):
    A = 0, 'A'
    B = 1, 'B'
    C = 2, 'C'
    D = 3, 'D'
    E = 4, 'E'
    F = 5, 'F'
    G = 6, 'G'
    H = 7, 'H'


class MatchLevel(models.IntegerChoices):
    PRELIMINARY = 0, _("Preliminary")
    ONE_SIXTEENTH = 1, _("1/16")
    ONE_EIGHTH = 2, _("1/8")
    SEMI_FINAL = 3, _("Semi Final")
    FiNAL = 4, _("Final")


class MatchStatus(models.IntegerChoices):
    NOT_STARTED = 2, _("Not Started")
    RUNNING = 0, _("Running")
    FINISHED = 1, _("Finished")
    INCOMPLETE = 3, _("Incomplete")


class WinnerChoices(models.IntegerChoices):
    TEAM_1 = 2, _("Team 1")
    TEAM_2 = 0, _("Team 2")
    DRAW = 1, _("Draw")


class TeamPlayerRole(models.IntegerChoices):
    GK = 0, "GK"
    LB = 1, "LB"
    RB = 2, "RB"
    LCB = 3, "LCB"
    RCB = 4, "RCB"
    CDM = 5, "CDM"
    LCM = 6, "LCM"
    RCM = 7, "RCM"
    RW = 8, "RW"
    LW = 9, "LW"
    ST = 10, "ST"
