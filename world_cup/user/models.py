import os
import pickle
import uuid

from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from common.models import BaseModel
from common.utils.time import get_now
from common.utils.validators import mobile_regex
from football.choices import WinnerChoices, MatchStatus
from football.models import Match


class User(AbstractUser, BaseModel):
    """Those who need to log into the system and profile must be a user in the first step,
        then their role is determined. All users must be enrolled in SSO.
        User token, medrick ID, mobile number, username, and email are received from SSO.
        First, the SSO must verify the player's identity and then register in the system.
        """

    def generate_token():
        return f'MED-{uuid.uuid4().hex[:6]}'

    token = models.CharField(verbose_name=_("Token"), max_length=255, null=True, blank=True, default=generate_token)
    mobile_number = models.CharField(verbose_name=_("Mobile number"), max_length=31, unique=True,
                                     validators=[mobile_regex], )

    REQUIRED_FIELDS = ['mobile_number']

    def __str__(self):
        return self.full_name

    @property
    def full_name(self):
        """Creates the users full name"""
        return f'{self.first_name} {self.last_name}' if self.first_name or self.last_name else self.username

    @property
    def player(self):
        try:
            player = cache.get(f'{Player.__module__}({self.pk})')
            if player:
                player = pickle.loads(player)
            else:
                player = Player.objects.filter(pk=self.pk).first()
        except:
            player = None

        cache.set(f'{Player.__module__}({self.pk})', pickle.dumps(player),
                  settings.CACHE_EXPIRATION_PLAYER_TIME)
        return player

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
                self.username = self.mobile_number
        super(User, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        """system_user and root can't delete"""
        if self.username in [os.environ.get('SYSTEM_USER_NAME'), os.environ.get('ROOT_USER_NAME')]:
            return super(User, self).delete(using=None, keep_parents=False)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class Player(User):
    def get_avatar():
        return {"current": "1"}

    avatar = models.JSONField(verbose_name=_('Avatar'), default=get_avatar, null=True, blank=True)
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
    """
        sample_predict_schema = {
                "arrange": [3, 4],
                "change_player": [3, 4],
                "yellow_card": [3, 4],
                "red_card": [3, 4],
                "goal": [3, 4],
                "assist_goal": [3, 4],
                "best_player": 3
        }
    """

    player = models.ForeignKey(to=Player, on_delete=models.CASCADE)
    match = models.ForeignKey(to=Match, on_delete=models.CASCADE)
    predict_team_1 = models.JSONField()
    predict_team_2 = models.JSONField()
    winner = models.IntegerField(verbose_name=_('winner'), choices=WinnerChoices.choices)
    is_penalty = models.BooleanField(verbose_name=_('is penalty'), default=False)

    point = models.PositiveIntegerField(verbose_name=_("score"), null=True, blank=True,
                                        help_text="Points earned from correct predictions.")

    class Meta:
        unique_together = ('player', 'match')

    def __str__(self):
        return f'{self.player.username} {self.match}'
