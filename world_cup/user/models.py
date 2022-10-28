import os
import pickle
import uuid

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser

from common.models import BaseModel
from common.utils.validators import mobile_regex
from football.choices import WinnerChoices
from football.models import Match, TeamPlayer


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

    score = models.PositiveBigIntegerField(verbose_name=_('score'), null=True, blank=True)

    def rank(self, query=None):
        if not query:
            query = Player.objects.all()

        queryset = query.filter(score__isnull=False).order_by('-score')
        if queryset:
            return list(queryset.values_list('pk', flat=True)).index(self.id) + 1
        return 0

    class Meta:
        verbose_name = _("Player")
        verbose_name_plural = _("Players")
        # indexes = ('score',)


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
    Before Match start players should send them predicts.
    """

    player = models.ForeignKey(verbose_name=_('player'), to=Player, on_delete=models.CASCADE)
    match = models.ForeignKey(verbose_name=_('match'), to=Match, on_delete=models.CASCADE)
    team_1_goals = models.PositiveIntegerField(verbose_name=_("team 1 goals"), )
    team_2_goals = models.PositiveIntegerField(verbose_name=_("team 2 goals"), )

    best_player = models.ForeignKey(verbose_name=_('best_player'), to=TeamPlayer, on_delete=models.CASCADE, null=True,
                                    blank=True)
    winner = models.IntegerField(verbose_name=_('winner'), choices=WinnerChoices.choices)
    is_penalty = models.BooleanField(verbose_name=_('is penalty'), default=False)

    arrange_1_list = ArrayField(verbose_name=_("arrange 1 list"), base_field=models.IntegerField(), default=list)
    arrange_2_list = ArrayField(verbose_name=_("arrange 2 list"), base_field=models.IntegerField(), default=list)
    goal_1_list = ArrayField(verbose_name=_("goal 1 list"), base_field=models.IntegerField(), default=list)
    goal_2_list = ArrayField(verbose_name=_("goal 2 list"), base_field=models.IntegerField(), default=list)
    goal_assist_1_list = ArrayField(verbose_name=_("goal assist 1 list"), base_field=models.IntegerField(),
                                    default=list)
    goal_assist_2_list = ArrayField(verbose_name=_("goal assist 2 list"), base_field=models.IntegerField(),
                                    default=list)
    yellow_card_1_list = ArrayField(verbose_name=_("yellow card 1 list"), base_field=models.IntegerField(),
                                    default=list)
    yellow_card_2_list = ArrayField(verbose_name=_("yellow card 2 list"), base_field=models.IntegerField(),
                                    default=list)
    red_card_1_list = ArrayField(verbose_name=_("red card 1 list"), base_field=models.IntegerField(), default=list)
    red_card_2_list = ArrayField(verbose_name=_("red card 2 list"), base_field=models.IntegerField(), default=list)
    change_1_list = ArrayField(verbose_name=_("change 1 list"), base_field=models.IntegerField(), default=list)
    change_2_list = ArrayField(verbose_name=_("change 2 list"), base_field=models.IntegerField(), default=list)

    point = models.IntegerField(verbose_name=_("score"), null=True, blank=True,
                                help_text="Points earned from correct predictions.")

    is_processed = models.BooleanField(verbose_name=_('is processed'), default=False,
                                       help_text='after all player predicts calculated change to True')

    class Meta:
        unique_together = ('player', 'match')

    def __str__(self):
        return f'{self.player.username} {self.match}'
