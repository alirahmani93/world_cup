from django.db.models.signals import post_save
from django.dispatch import receiver

from common.models import CorrectPredictScore
from football.choices import MatchStatus
from football.models import MatchResult, Match

from user.models import PredictionArrange


@receiver(post_save, sender=Match)
def update_concurrent_players(sender, instance, *args, **kwargs) -> None:
    print("update_concurrent_players")
    calculate(match=instance)


def calculate(match):
    if match.status != MatchStatus.FINISHED:
        return

    result: MatchResult = match.matchresult
    cp = CorrectPredictScore.load()
    print('----------------------' * 5)
    print(result)

    predicts = PredictionArrange.objects.filter(match=match, is_processed=False)
    print(predicts)
    for predict in predicts:
        print('----------------------')
        points = 0

        bpi = result.best_player_id == predict.best_player.id
        points += cp.best_player_score if bpi else cp.best_player_negative_score

        penalty = result.is_penalty == predict.is_penalty
        points += cp.penalty_score if penalty else cp.penalty_negative_score

        winner = result.winner == predict.winner
        points += cp.best_player_score if winner else cp.correct_winner_negative_score

        gt1 = result.team_1_goals == predict.team_1_goals
        gt2 = result.team_2_goals == predict.team_2_goals
        points += cp.final_result_score if gt1 and gt2 else cp.final_result_negative_score

        ar1 = result.arrange_1_list == predict.arrange_1_list
        points += cp.arrange_score if ar1 else cp.arrange_negative_score
        ar2 = result.arrange_2_list == predict.arrange_2_list
        points += cp.arrange_score if ar2 else cp.arrange_negative_score

        ga1 = result.goal_assist_1_list == predict.goal_assist_1_list
        points += cp.assist_goal_score if ga1 else cp.assist_goal_negative_score
        ga2 = result.goal_assist_2_list == predict.goal_assist_2_list
        points += cp.assist_goal_score if ga2 else cp.assist_goal_negative_score

        yc1 = result.yellow_card_1_list == predict.yellow_card_1_list
        points += cp.yellow_card_score if yc1 else cp.yellow_card_negative_score
        yc2 = result.yellow_card_2_list == predict.yellow_card_2_list
        points += cp.yellow_card_score if yc2 else cp.yellow_card_negative_score

        gs1 = result.goal_1_list == predict.goal_1_list
        points += cp.goal_score if gs1 else cp.goal_negative_score
        gs2 = result.goal_2_list == predict.goal_2_list
        points += cp.goal_score if gs2 else cp.goal_negative_score

        rc1 = result.red_card_1_list == predict.red_card_1_list
        points += cp.red_card_score if rc1 else cp.red_card_negative_score
        rc2 = result.red_card_2_list == predict.red_card_2_list
        points += cp.red_card_score if rc2 else cp.red_card_negative_score

        ch1 = result.change_1_list == predict.change_1_list
        points += cp.change_player_score if ch1 else cp.change_player_negative_score
        ch2 = result.change_2_list == predict.change_2_list
        points += cp.change_player_score if ch2 else cp.change_player_negative_score

        predict.point = points
        predict.is_processed = True
        predict.save()

        predict.player.score += points
        predict.player.save()
        print(predict.player.score, predict.point)
        print(f'\x1b[0;37;40m {predict.player.username} points:', points)

    result.is_processed = True
    result.save()
