from rest_framework.views import status

OK_200 = {
    'detail': 'OK',
    'code': 'OK',
    'number': status.HTTP_200_OK
}
PLAYER_NOT_FOUND_450 = {
    'detail': 'Player not found',
    'code': 'player_not_found',
    'number': 450
}
MATCH_NOT_FOUND_451 = {
    'detail': 'Match not found',
    'code': 'match_not_found',
    'number': 451
}
