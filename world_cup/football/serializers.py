from rest_framework import serializers

from common.serializers import excluded_fields, BaseModelSerializer
from common.utils.time import standard_response_datetime
from .models import Match, TeamPlayer, Team


class TeamSerializer(BaseModelSerializer):
    class Meta:
        model = Team
        exclude = excluded_fields


class TeamPlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamPlayer
        exclude = excluded_fields


class MatchSerializer(serializers.ModelSerializer):
    team_1 = TeamSerializer(many=False)
    team_2 = TeamSerializer(many=False)
    start_time = serializers.SerializerMethodField()
    end_time = serializers.SerializerMethodField()

    class Meta:
        model = Match
        exclude = excluded_fields

    def get_start_time(self, obj):
        return standard_response_datetime(obj.start_time)

    def get_end_time(self, obj):
        if obj.end_time:
            return standard_response_datetime(obj.end_time)


class TeamWithTeamPlayerSerializer(TeamSerializer):
    players = serializers.SerializerMethodField()

    class Meta:
        model = Team
        exclude = excluded_fields

    def get_players(self, obj):
        players = obj.teamplayer_set.filter(is_active=True)
        if players.exists():
            return TeamPlayerSerializer(players, many=True).data
        return dict()
