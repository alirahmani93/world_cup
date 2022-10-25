from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from common.models import BaseModel
from football.choices import Continent, WorldCupGroup, MatchLevel, MatchStatus, WinnerChoices, TeamPlayerRole


class Team(BaseModel):
    name = models.CharField(verbose_name=_('name'), max_length=255)
    continent = models.IntegerField(verbose_name=_('continent'), choices=Continent.choices)
    group = models.IntegerField(verbose_name=_("group"), choices=WorldCupGroup.choices)
    current_level = models.IntegerField(verbose_name=_("current level"), choices=MatchLevel.choices,
                                        default=MatchLevel.PRELIMINARY)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Team")
        verbose_name_plural = _("Teams")


class TeamPlayer(BaseModel):
    first_name = models.CharField(verbose_name=_('first name'), max_length=255)
    last_name = models.CharField(verbose_name=_('last name'), max_length=255)
    number = models.PositiveBigIntegerField(verbose_name=_('number'), validators=[MaxValueValidator(100)])
    team = models.ForeignKey(verbose_name=_('team'), to=Team, on_delete=models.CASCADE)
    is_banned_next_match = models.BooleanField(verbose_name=_("is banned next match"), default=False)
    rank = models.FloatField(verbose_name=_("rank"), validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name}({self.team})'

    class Meta:
        unique_together = ['first_name', 'last_name', 'team']


class Match(BaseModel):
    team_1 = models.ForeignKey(verbose_name=_('team 1'), to=Team, on_delete=models.CASCADE, related_name='team1')
    team_2 = models.ForeignKey(verbose_name=_('team 2'), to=Team, on_delete=models.CASCADE, related_name='team2')

    start_time = models.DateTimeField(verbose_name=_('start time'), )
    end_time = models.DateTimeField(verbose_name=_('end time'), blank=True, null=True, )

    level = models.IntegerField(verbose_name=_("level"), choices=MatchLevel.choices)
    status = models.IntegerField(verbose_name=_("status"), choices=MatchStatus.choices, default=MatchStatus.NOT_STARTED)

    winner = models.IntegerField(verbose_name=_("winner"), choices=WinnerChoices.choices, blank=True, null=True)
    is_penalty = models.BooleanField(verbose_name=_('is penalty'), default=False)

    def __str__(self):
        return f'{self.team_1}-{self.team_2} ({self.level})'

    def save(self, *args, **kwargs):
        if self.status == MatchStatus.NOT_STARTED:
            if self.winner:
                raise Exception(_("Match Not start yet so winner side is not acceptable."))
        if self.level != MatchLevel.PRELIMINARY:
            if self.winner == WinnerChoices.DRAW:
                raise Exception("Draw in this level impossible!")
        super(Match, self).save(args, kwargs)

        if self.status == MatchStatus.FINISHED:
            self.match_finish()

    class Meta:
        verbose_name = _("Match")
        verbose_name_plural = _("Matches")

    def match_finish(self):
        r1, r2 = self.calculate_match_result()
        MatchResult.objects.create(match=self, winner=self.winner, team_1=r1, team_2=r2, is_penalty=self.is_penalty)
        print('match result created')

    def calculate_match_result(self):
        team_players_1 = TeamPlayerAction.objects.filter(player__team=self.team_1)
        team_players_2 = TeamPlayerAction.objects.filter(player__team=self.team_2)

        result_team_1 = self.calculate_match_player_result(team_players_1)
        result_team_2 = self.calculate_match_player_result(team_players_2)
        return result_team_1, result_team_2

    @staticmethod
    def calculate_match_player_result(team_players):
        tmp = []
        for tp in team_players:
            tmp.append(tp.make_dict())
        return tmp


class TeamPlayerAction(BaseModel):
    match = models.ForeignKey(verbose_name=_('match'), to=Match, on_delete=models.CASCADE)
    player = models.ForeignKey(verbose_name=_('player'), to=TeamPlayer, on_delete=models.CASCADE)
    role = models.IntegerField(verbose_name=_("role"), choices=TeamPlayerRole.choices)

    yellow_card = models.PositiveSmallIntegerField(verbose_name=_("yellow card"), default=0,
                                                   validators=[MaxValueValidator(2)])
    red_card = models.BooleanField(verbose_name=_("red card"), default=False, )

    goal = models.PositiveSmallIntegerField(verbose_name=_("goal"), default=0, )
    assist_goal = models.PositiveSmallIntegerField(verbose_name=_("assist goal"), default=0, )

    is_change = models.BooleanField(verbose_name=_("is change"), default=False, )
    is_best_player = models.BooleanField(verbose_name=_("is best player"), default=False)

    class Meta:
        verbose_name = _("Action Team Player")
        verbose_name_plural = _("Action Team Players")
        unique_together = ('match', 'player')

    def __str__(self):
        return f'{self.player.full_name} ({self.match})'

    def make_dict(self):
        return {
            'match': self.match.id,
            'player': self.player.id,
            'team': self.player.team.id,
            'yellow_card': self.yellow_card,
            'goal': self.goal,
            'assist_goal': self.assist_goal,

            'red_card': self.red_card,
            'is_change': self.is_change,
            'is_best_player': self.is_best_player,
        }


class MatchResult(BaseModel):
    match = models.OneToOneField(verbose_name=_("match"), to=Match, on_delete=models.CASCADE)
    winner = models.IntegerField(verbose_name=_("winner"), choices=WinnerChoices.choices)
    is_penalty = models.BooleanField(verbose_name=_('is penalty'), default=False)
    team_1 = models.JSONField(verbose_name=_("team 1"), )
    team_2 = models.JSONField(verbose_name=_("team 2"), )

    class Meta:
        verbose_name = _("Match Result")
        verbose_name_plural = _("Match Results")

    def __str__(self):
        return f'result ( {self.match} )'
