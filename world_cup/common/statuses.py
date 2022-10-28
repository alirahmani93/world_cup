from rest_framework.views import status

OK_200 = {
    'detail': 'OK',
    'code': 'OK',
    'number': status.HTTP_200_OK
}
# 400
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

INVALID_OTP_460 = {
    'detail': 'Invalid OTP',
    'code': 'invalid_otp',
    'number': status.HTTP_403_FORBIDDEN
}

OTP_NOT_FOUND_461 = {
    'detail': 'OTP not found',
    'code': 'otp_not_found',
    'number': 461
}

PREDICTION_TIME_OVER_470 = {
    'detail': 'Prediction time is over',
    'code': 'prediction_time_is_over',
    'number': 470
}
