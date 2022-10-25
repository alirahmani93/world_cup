from common.models import CorrectPredictScore
from football.models import MatchResult


def calculate_points(predict: dict, match_players):
    cp = CorrectPredictScore.load()
    mr = MatchResult.objects.filter()
    keys = ['arrange', 'change_player', 'yellow_card', 'red_card', 'goal', 'assist_goal', ]

    arrange_ids = match_players.values_list('player_id', flat=True)
    red_card_ids = match_players.filter(red_card=True).values_list('player_id', flat=True)
    is_change_ids = match_players.filter(is_change=True).values_list('player_id', flat=True)
    is_best_player_id = match_players.filter(is_best_player=True).values_list('player_id', flat=True)

    yellow_card_ids = match_players.filter(yellow_card__gt=0).values('player_id', 'yellow_card')
    goal_ids = match_players.filter(goal__gt=0).values('player_id', 'goal')
    assist_goal_ids = match_players.filter(assist_goal__gt=0).values('player_id', 'assist_goal')

    x = {
        "arrange": arrange_ids,
        "red_card": red_card_ids,
        "best_player": is_best_player_id,
        "change_player": is_change_ids,

        "yellow_card": [3, 4],
        "goal": [3, 4],
        "assist_goal": [3, 4]
    }
    print(x)
    point = 0
    # if predict['arrange'] == arrange_ids:
    #     point += cp.arrange_score
    #
    # for i in red_card_ids:
    #     if i in predict['red_card']:
    #         point += cp.yellow_card_score
    #
    # for i in is_change_ids:
    #     if i == predict['is_change']:
    #         point += cp.change_player_score
    #
    # if predict['is_best_player'] == is_best_player_id:
    #     point += cp.best_player_score
    #
    # ####
    # for i in yellow_card_ids:
    #     if i['player_id'] in predict['yellow_card']:
    #         if i['yellow_card'] ==
    #             point += cp.yellow_card_score
    #
    # for i in goal_ids:
    #     if i in predict['goal']:
    #         point += cp.goal_score
    #
    # for i in assist_goal_ids:
    #     if i in predict['assist_goal']:
    #         point += cp.assist_goal_score

    return point
