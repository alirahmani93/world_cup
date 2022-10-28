from django.contrib.postgres.fields import ArrayField
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from common.models import BaseModel
from common.utils.time import get_now
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
        return f'{self.team_1}-{self.team_2} (level:{self.level})'

    def save(self, *args, **kwargs):
        if self.status == MatchStatus.NOT_STARTED:
            if self.winner:
                raise Exception(_("Match Not start yet so winner side is not acceptable."))
        if self.level != MatchLevel.PRELIMINARY:
            if self.winner == WinnerChoices.DRAW:
                raise Exception("Draw in this level impossible!")
        if self.status == MatchStatus.FINISHED:
            print(self.teamplayeraction_set.filter(is_best_player=True).count())
            if self.teamplayeraction_set.filter(is_best_player=True).count() != 1:
                raise ValueError('One Player must be a best player')

            if not self.winner:
                raise Exception("Who is winner?!")
            self.match_finish()
        super(Match, self).save(args, kwargs)

    class Meta:
        verbose_name = _("Match")
        verbose_name_plural = _("Matches")

    def match_finish(self):
        t1 = get_now()

        team_players_1 = self.teamplayeraction_set.filter(player__team=self.team_1)
        team_players_2 = self.teamplayeraction_set.filter(player__team=self.team_2)

        tg_1, bpi_1, gl_1, ga_1, ar_1, ch_1, yc_1, rc_1 = self.calculate_match_player_result(team_players_1)
        tg_2, bpi_2, gl_2, ga_2, ar_2, ch_2, yc_2, rc_2 = self.calculate_match_player_result(team_players_2)
        bpi = bpi_1 if bpi_1 else bpi_2

        x = MatchResult.objects.filter(match=self, )
        if x.exists():
            x.update(
                winner=self.winner,
                is_penalty=self.is_penalty,
                best_player_id=bpi,
                team_1_goals=tg_1,
                team_2_goals=tg_2,
                arrange_1_list=ar_1,
                arrange_2_list=ar_2,
                goal_1_list=gl_1,
                goal_2_list=gl_2,
                goal_assist_1_list=ga_1,
                goal_assist_2_list=ga_2,
                yellow_card_1_list=yc_1,
                yellow_card_2_list=yc_2,
                red_card_1_list=rc_1,
                red_card_2_list=rc_2,
                change_1_list=ch_1,
                change_2_list=ch_2,
            )
        else:
            MatchResult.objects.create(
                match=self,
                winner=self.winner,
                is_penalty=self.is_penalty,
                best_player_id=bpi,
                team_1_goals=tg_1,
                team_2_goals=tg_2,
                arrange_1_list=ar_1,
                arrange_2_list=ar_2,
                goal_1_list=gl_1,
                goal_2_list=gl_2,
                goal_assist_1_list=ga_1,
                goal_assist_2_list=ga_2,
                yellow_card_1_list=yc_1,
                yellow_card_2_list=yc_2,
                red_card_1_list=rc_1,
                red_card_2_list=rc_2,
                change_1_list=ch_1,
                change_2_list=ch_2,
            )

        print(f'{self.__str__()}: MatchResult created at:{get_now()}')
        print(f'Process time :{get_now() - t1}') \

    @staticmethod
    def calculate_match_player_result(team_players_action):
        best_player_id = 0
        total_goal = 0
        goals = []
        assist_goals = []
        arrange = []
        changes = []
        yellow_cards = []
        red_cards = []
        for tp in team_players_action:
            print('>>>>>>>', tp.goal, tp.assist_goal, tp.yellow_card)
            arrange.append(tp.id)
            total_goal += tp.goal

            if tp.goal:
                goals.append(tp.id)
            if tp.assist_goal:
                assist_goals.append(tp.id)
            if tp.yellow_card:
                yellow_cards.append(tp.id)
            if tp.red_card:
                red_cards.append(tp.id)
            if tp.is_change:
                changes.append(tp.id)

            if not best_player_id:
                if tp.is_best_player:
                    best_player_id = tp.player.id

        return (
            total_goal,
            best_player_id,
            sorted(goals),
            sorted(assist_goals),
            sorted(arrange),
            sorted(changes),
            sorted(yellow_cards),
            sorted(red_cards)
        )


class TeamPlayerAction(BaseModel):
    match = models.ForeignKey(verbose_name=_('match'), to=Match, on_delete=models.CASCADE)
    player = models.ForeignKey(verbose_name=_('player'), to=TeamPlayer, on_delete=models.CASCADE)
    role = models.IntegerField(verbose_name=_("role"), choices=TeamPlayerRole.choices)

    yellow_card = models.BooleanField(verbose_name=_("yellow card"), default=False)
    red_card = models.BooleanField(verbose_name=_("red card"), default=False, )

    goal = models.PositiveSmallIntegerField(verbose_name=_("goal"), default=0, )
    assist_goal = models.PositiveSmallIntegerField(verbose_name=_("assist goal"), default=0, )

    is_change = models.BooleanField(verbose_name=_("is change"), default=False, )
    is_best_player = models.BooleanField(verbose_name=_("is best player"), default=False)

    @property
    def team_name(self) -> str:
        return self.player.team.name

    def save(self, *args, **kwargs):
        super(TeamPlayerAction, self).save(args, kwargs)

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
    team_1_goals = models.PositiveIntegerField(verbose_name=_("team 1 goals"), )
    team_2_goals = models.PositiveIntegerField(verbose_name=_("team 2 goals"), )
    best_player_id = models.IntegerField(verbose_name=_("best player id"))

    arrange_1_list = ArrayField(verbose_name=_("arrange 1 list"), base_field=models.IntegerField())
    arrange_2_list = ArrayField(verbose_name=_("arrange 2 list"), base_field=models.IntegerField())
    goal_1_list = ArrayField(verbose_name=_("goal 1 list"), base_field=models.IntegerField())
    goal_2_list = ArrayField(verbose_name=_("goal 2 list"), base_field=models.IntegerField())
    goal_assist_1_list = ArrayField(verbose_name=_("goal assist 1 list"), base_field=models.IntegerField())
    goal_assist_2_list = ArrayField(verbose_name=_("goal assist 2 list"), base_field=models.IntegerField())
    yellow_card_1_list = ArrayField(verbose_name=_("yellow card 1 list"), base_field=models.IntegerField())
    yellow_card_2_list = ArrayField(verbose_name=_("yellow card 2 list"), base_field=models.IntegerField())
    red_card_1_list = ArrayField(verbose_name=_("red card 1 list"), base_field=models.IntegerField())
    red_card_2_list = ArrayField(verbose_name=_("red card 2 list"), base_field=models.IntegerField())
    change_1_list = ArrayField(verbose_name=_("change 1 list"), base_field=models.IntegerField())
    change_2_list = ArrayField(verbose_name=_("change 2 list"), base_field=models.IntegerField())

    is_processed = models.BooleanField(verbose_name=_('is processed'), default=False,
                                       help_text='after all player predicts calculated change to True')

    # def save(self,*args,**kwargs):

    class Meta:
        verbose_name = _("Match Result")
        verbose_name_plural = _("Match Results")

    def __str__(self):
        return f'result ( {self.match} )'
