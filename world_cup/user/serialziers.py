from rest_framework import serializers

from common.serializers import BaseSerializer
from user.models import PredictionArrange, Player


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        exclude = ['user_permissions', 'groups', 'token', 'password', 'is_superuser', 'is_staff']
        extra_kwargs = {
            'is_blocked': {'read_only': True},
            'is_verified': {'read_only': True},
            'is_active': {'read_only': True},

        }


class TeamPredictSerializer(BaseSerializer):
    arrange = serializers.ListField()
    change_player = serializers.ListField()
    yellow_card = serializers.ListField()
    red_card = serializers.ListField()
    goal = serializers.ListField()
    assist_goal = serializers.ListField()

    penalty = serializers.BooleanField()


class PredictSerializer(serializers.ModelSerializer):
    predict_team_1 = TeamPredictSerializer()
    predict_team_2 = TeamPredictSerializer()

    class Meta:
        model = PredictionArrange
        exclude = []
