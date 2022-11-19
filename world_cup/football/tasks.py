from celery import shared_task

from common.models import CorrectPredictScore
from football.choices import MatchStatus
from football.models import MatchResult, Match
from user.models import PredictionArrange


def item_calculator(condition, filed_name: str, positive_point, negative_point, predict_: PredictionArrange, points):
    if condition:
        predict_.points_detail[filed_name] = positive_point
        points += positive_point
    else:
        predict_.points_detail[filed_name] = negative_point
        points += negative_point
    return predict_, points


@shared_task(name='calculate_match_check_out')
def calculate(match):
    try:
        match = Match.objects.get(id=match)
        # print(match)
        if not match:
            print(f'match id:{match} is not found')
            return
        if match.status != MatchStatus.FINISHED:
            return

        result: MatchResult = match.matchresult
        cp = CorrectPredictScore.load()
        # print('----------------------' * 5)
        # print(result)

        predicts = PredictionArrange.objects.filter(match=match, is_processed=False)
        # print(predicts)
        for predict in predicts:
            print('----------------------')
            points = 0

            predict, points = item_calculator(
                condition=result.best_player_id == predict.best_player.id,
                filed_name='best_player_id',
                positive_point=cp.best_player_score,
                negative_point=cp.best_player_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.is_penalty == predict.is_penalty,
                filed_name='is_penalty',
                positive_point=cp.penalty_score,
                negative_point=cp.penalty_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.winner == predict.winner,
                filed_name='winner',
                positive_point=cp.correct_winner_score,
                negative_point=cp.correct_winner_negative_score,
                predict_=predict,
                points=points)

            gt1 = result.team_1_goals == predict.team_1_goals
            gt2 = result.team_2_goals == predict.team_2_goals
            predict, points = item_calculator(
                condition=gt1 and gt2,
                filed_name='final_result',
                positive_point=cp.final_result_score,
                negative_point=cp.final_result_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.arrange_1_list == predict.arrange_1_list,
                filed_name='arrange_1_list',
                positive_point=cp.arrange_score,
                negative_point=cp.arrange_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.arrange_2_list == predict.arrange_2_list,
                filed_name='arrange_2_list',
                positive_point=cp.arrange_score,
                negative_point=cp.arrange_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.goal_assist_1_list == predict.goal_assist_1_list,
                filed_name='goal_assist_1_list',
                positive_point=cp.assist_goal_score,
                negative_point=cp.assist_goal_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.goal_assist_2_list == predict.goal_assist_2_list,
                filed_name='goal_assist_2_list',
                positive_point=cp.assist_goal_score,
                negative_point=cp.assist_goal_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.yellow_card_1_list == predict.yellow_card_1_list,
                filed_name='yellow_card_1_list',
                positive_point=cp.yellow_card_score,
                negative_point=cp.yellow_card_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.yellow_card_2_list == predict.yellow_card_2_list,
                filed_name='yellow_card_2_list',
                positive_point=cp.yellow_card_score,
                negative_point=cp.yellow_card_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.goal_1_list == predict.goal_1_list,
                filed_name='goal_1_list',
                positive_point=cp.goal_score,
                negative_point=cp.goal_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.goal_2_list == predict.goal_2_list,
                filed_name='goal_2_list',
                positive_point=cp.goal_score,
                negative_point=cp.goal_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.red_card_1_list == predict.red_card_1_list,
                filed_name='red_card_1_list',
                positive_point=cp.red_card_score,
                negative_point=cp.red_card_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.red_card_2_list == predict.red_card_2_list,
                filed_name='red_card_2_list',
                positive_point=cp.red_card_score,
                negative_point=cp.red_card_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.change_1_list == predict.change_1_list,
                filed_name='change_1_list',
                positive_point=cp.change_player_score,
                negative_point=cp.change_player_negative_score,
                predict_=predict,
                points=points)

            predict, points = item_calculator(
                condition=result.change_2_list == predict.change_2_list,
                filed_name='change_2_list',
                positive_point=cp.change_player_score,
                negative_point=cp.change_player_negative_score,
                predict_=predict,
                points=points)

            predict.point = points
            predict.is_processed = True
            predict.save()

            predict.player.score += points
            predict.player.save()
            print(predict.player.score, predict.point)
            print(f'\x1b[0;37;40m {predict.player.username} points:', points)

        result.is_processed = True
        result.save()
        print('DONE')
    except Exception as e:
        print(e.__str__())
