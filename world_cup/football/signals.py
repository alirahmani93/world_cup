from football.choices import MatchStatus
from football.models import Match, TeamPlayerAction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, Min
from django.core.cache import cache
from django.conf import settings

from football.prediction import calculate_points
from user.models import Player, PredictionArrange


@receiver(post_save, sender=Match)
def update_concurrent_players(sender, instance, *args, **kwargs) -> None:
    print("update_concurrent_players")
    if not instance.status == MatchStatus.FINISHED:
        return

    match_players = TeamPlayerAction.objects.filter(match=instance).select_related('player')

    team_1 = match_players.filter(player__team=instance.team_1)
    # team_2 = match_players.filter(player__team=instance.team_2)

    predicts = PredictionArrange.objects.filter(match=instance)
    for predict in predicts:
        point_1 = calculate_points(predict=predict.predict_team_1, match_players=team_1, )
        # point_2 = calculate_points(predict=predict.predict_team_2, match_players=team_2)
        points = point_1  # + point_2

        # post_save.disconnect(update_concurrent_players, sender=Match)
        # predict.point = points
        # predict.save()
        #
        # predict.player.score += points
        # predict.player.save()
        # post_save.connect(update_concurrent_players, sender=Match)
