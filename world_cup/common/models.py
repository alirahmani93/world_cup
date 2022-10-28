from uuid import uuid4
from django.core.validators import MaxValueValidator
from django.conf import settings
from django.core.cache import cache
from django.db import models
from django.utils.translation import gettext_lazy as _

from common.choices import SMSModeKeys
from common.utils.time import standard_response_datetime, get_now
from common.utils.validators import version_regex


# Create your models here.


class BaseModel(models.Model):
    """All models in project inherit. These parameters are necessary. """
    uuid = models.UUIDField(verbose_name=_("UUID"), editable=False, default=uuid4)
    is_active = models.BooleanField(verbose_name=_("Is active"), default=True)
    updated_time = models.DateTimeField(verbose_name=_("Updated time"), auto_now=True)
    created_time = models.DateTimeField(verbose_name=_("Created time"), auto_now_add=True)

    def __str__(self):
        return f"{self.uuid}"

    class Meta:
        abstract = True


class SingletonBaseModel(BaseModel):
    """Used to ensure that a class can only have one concurrent instance."""

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.__class__.objects.count() == 1:
                raise Exception(_('Only one instance of configurations is allowed.'))
            self.created_time = get_now()
        super().save(*args, **kwargs)


class Configuration(SingletonBaseModel):
    """
        System configuration have some data are use in other entity and specifications.
    properties return static data at project
    """

    def get_app_name():
        return settings.PROJECT_NAME

    app_name = models.CharField(verbose_name=_("App Name"), max_length=255, default=get_app_name)
    deep_link_prefix = models.CharField(verbose_name=_("Deep link prefix"), max_length=255, blank=True, default='')
    maintenance_mode = models.BooleanField(verbose_name=_('Maintenance mode'), default=False)

    app_version = models.CharField(
        verbose_name=_("App Version"), max_length=100, default='1.0.0', validators=[version_regex])
    app_version_bundle = models.PositiveIntegerField(verbose_name=_("app version bundle"), default=1)
    last_bundle_version = models.PositiveIntegerField(verbose_name=_("Last bundle version"), default=1)
    minimum_supported_bundle_version = models.PositiveIntegerField(
        verbose_name=_("minimum supported bundle version"), default=1, )
    by_pass_sms = models.BooleanField(verbose_name=_("by pass sms"), default=False)

    @property
    def server_time_zone(self):
        return settings.TIME_ZONE

    @property
    def server_time(self):
        return standard_response_datetime(get_now())

    @property
    def choices_continent(self):
        from football.choices import Continent
        return Continent.choices

    @property
    def choices_world_cup_group(self):
        from football.choices import WorldCupGroup
        return WorldCupGroup.choices

    @property
    def choices_match_level(self):
        from football.choices import MatchLevel
        return MatchLevel.choices

    @property
    def choices_match_status(self):
        from football.choices import MatchStatus
        return MatchStatus.choices

    @property
    def choices_winner(self):
        from football.choices import WinnerChoices
        return WinnerChoices.choices

    @property
    def choices_team_player_role(self):
        from football.choices import TeamPlayerRole
        return TeamPlayerRole.choices

    @classmethod
    def load(cls):
        cache_data = cache.get(settings.CONFIGURATION_PREFIX)
        if cache_data:
            return cache_data
        data = cls.objects.get_or_create()[0]
        cache.set(settings.CONFIGURATION_PREFIX, data)
        return data

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.set(settings.CONFIGURATION_PREFIX, self)


class CorrectPredictScore(SingletonBaseModel):
    arrange_score = models.PositiveIntegerField(verbose_name=_("arrange score"), default=1)
    change_player_score = models.PositiveIntegerField(verbose_name=_("change player score"), default=1)
    goal_score = models.PositiveIntegerField(verbose_name=_("goal score"), default=1)
    yellow_card_score = models.PositiveIntegerField(verbose_name=_("yellow card score"), default=1)
    red_card_score = models.PositiveIntegerField(verbose_name=_("red_card score"), default=1)
    correct_winner_score = models.PositiveIntegerField(verbose_name=_("correct winner score"), default=1)
    final_result_score = models.PositiveIntegerField(verbose_name=_("final result score"), default=1)
    assist_goal_score = models.PositiveIntegerField(verbose_name=_("assist goal score"), default=1)
    best_player_score = models.PositiveIntegerField(verbose_name=_("best player score"), default=1)
    penalty_score = models.PositiveIntegerField(verbose_name=_("penalty score"), default=1)
    # Negative points
    arrange_negative_score = models.IntegerField(verbose_name=_("arrange negative score"), default=-1,
                                                 validators=[MaxValueValidator(0)])
    change_player_negative_score = models.IntegerField(verbose_name=_("change player negative score"),
                                                       default=-1, validators=[MaxValueValidator(0)])
    goal_negative_score = models.IntegerField(verbose_name=_("goal negative score"), default=-1,
                                              validators=[MaxValueValidator(0)])
    yellow_card_negative_score = models.IntegerField(verbose_name=_("yellow card negative score"), default=-1,
                                                     validators=[MaxValueValidator(0)])
    red_card_negative_score = models.IntegerField(verbose_name=_("red_card negative score"), default=-1,
                                                  validators=[MaxValueValidator(0)])
    correct_winner_negative_score = models.IntegerField(verbose_name=_("correct winner negative score"),
                                                        default=-1, validators=[MaxValueValidator(0)])
    final_result_negative_score = models.IntegerField(verbose_name=_("final result negative score"), default=-1,
                                                      validators=[MaxValueValidator(0)])
    assist_goal_negative_score = models.IntegerField(verbose_name=_("assist goal negative score"), default=-1,
                                                     validators=[MaxValueValidator(0)])
    best_player_negative_score = models.IntegerField(verbose_name=_("best player negative score"), default=-1,
                                                     validators=[MaxValueValidator(0)])
    penalty_negative_score = models.IntegerField(verbose_name=_("penalty negative score"), default=-1,
                                                 validators=[MaxValueValidator(0)])

    def mapper(self):
        return {
            'arrange_score': self.arrange_score,
            'change_player_score': self.change_player_score,
            'goal_score': self.goal_score,
            'yellow_card_score': self.yellow_card_score,
            'red_card_score': self.red_card_score,
            'correct_winner_score': self.correct_winner_score,
            'final_result_score': self.final_result_score,
            'assist_goal_score': self.assist_goal_score,
            'best_player_score': self.best_player_score,

            'arrange_negative_score': self.arrange_negative_score * -1,
            'change_player_negative_score': self.change_player_negative_score * -1,
            'goal_negative_score': self.goal_negative_score * -1,
            'yellow_card_negative_score': self.yellow_card_negative_score * -1,
            'red_card_negative_score': self.red_card_negative_score * -1,
            'correct_winner_negative_score': self.correct_winner_negative_score * -1,
            'final_result_negative_score': self.final_result_negative_score * -1,
            'assist_goal_negative_score': self.assist_goal_negative_score * -1,
            'best_player_negative_score': self.best_player_negative_score * -1,
        }

    class Meta:
        verbose_name = _("Correct Predict Score")
        verbose_name_plural = _("Correct Predict Scores")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.set(settings.CORRECT_PREDICTION_SCORE_PREFIX, self)

    @classmethod
    def load(cls):
        cache_data = cache.get(settings.CORRECT_PREDICTION_SCORE_PREFIX)
        if cache_data:
            return cache_data
        data = cls.objects.get_or_create()[0]
        cache.set(settings.CORRECT_PREDICTION_SCORE_PREFIX, data)
        return data
