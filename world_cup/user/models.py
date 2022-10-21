import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from common.models import BaseModel
from common.utils.validators import mobile_regex
from football.models import Match
from user.choices import Gender


class User(AbstractUser, BaseModel):
    """Those who need to log into the system and profile must be a user in the first step,
        then their role is determined. All users must be enrolled in SSO.
        User token, medrick ID, mobile number, username, and email are received from SSO.
        First, the SSO must verify the player's identity and then register in the system.
        """
    token = models.CharField(verbose_name=_("Token"), max_length=255, null=True, blank=True)
    mobile_number = models.CharField(verbose_name=_("Mobile number"), max_length=31, unique=True,
                                     validators=[mobile_regex], )

    REQUIRED_FIELDS = ['mobile_number']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        """Creates the users full name"""
        return f'{self.first_name} {self.last_name}' if self.first_name or self.last_name else self.username

    @staticmethod
    def system_user():
        """system_user is a special user that has the ability to perform automatic operations"""
        system_user, is_created = User.objects.get_or_create(
            username=settings.SYSTEM_USER_NAME,
            mobile_number=settings.SYSTEM_USER_MOBILE_NUMBER,
            email=settings.SYSTEM_USER_EMAIL,
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        return system_user

    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.username:
                self.username = self.medrick_id
        super(User, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """system_user and root can't delete"""
        if self.username in [os.environ.get('SYSTEM_USER_NAME')]:
            return super(User, self).delete(using=None, keep_parents=False)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Player(User):
    avatar = models.JSONField(verbose_name=_('Avatar'), default={"current": "1"}, null=True, blank=True)
    profile_name = models.CharField(verbose_name=_("Profile name"), max_length=150, null=True, blank=True)

    is_verified = models.BooleanField(verbose_name=_('Is verified'), default=False)
    is_blocked = models.BooleanField(verbose_name=_('Is blocked'), default=False)

    setting = models.JSONField(verbose_name=_("Setting"), default=dict, null=True, blank=True)

    client_version = models.PositiveIntegerField(verbose_name=_("Client version"), default=0, null=True, blank=True)

    score = models.PositiveBigIntegerField(verbose_name=_('score'))

    class Meta:
        verbose_name = _("Player")
        verbose_name_plural = _("Players")


class Feedback(BaseModel):
    """Any player can send feedback from Apk.
     Usually, they use this mechanism when a bug occurs in the system or when they want to express their opinion
     to the developers. """
    player = models.ForeignKey(verbose_name=_("player"), to=Player, on_delete=models.CASCADE)
    description = models.TextField(verbose_name=_("description"))
    is_resolved = models.BooleanField(verbose_name=_("is resolved"), default=False)

    def __str__(self):
        return f'{self.player.username}: {self.short_description}'

    class Meta:
        verbose_name = _("Feed Back")
        verbose_name_plural = _("Feed Backs")
        ordering = ['-created_time', ]

    @property
    def short_description(self):
        return f'{self.description[:20]}...'


class PredictionArrange(BaseModel):
    player = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    match = models.ForeignKey(to=Match, on_delete=models.CASCADE)
    predict_team_1 = models.JSONField()
    predict_team_2 = models.JSONField()

    sample_predict = {
        'arrange': {
            'gk': 'team_player_id',
            'rb': 'team_player_id',
            'lb': 'team_player_id',
            'lcb': 'team_player_id',
            'rcb': 'team_player_id',
            'cdm': 'team_player_id',
            'lcm': 'team_player_id',
            'rcm': 'team_player_id',
            'rw': 'team_player_id',
            'lw': 'team_player_id',
            'st': 'team_player_id',
        },  # or 'arrange':['id[int]']
        'change_player': ['id[int]'],
        'yellow_card': ['id[int]'],
        'red_card': ['id[int]'],
        'goal': ['id[int]'],
        'assist_goal': ['id[int]'],
        'winner': 'Enum[team1 or team2 or draw]',
        'penalty': '[bool]',
    }

    class Meta:
        unique_together = ('player', 'match')
