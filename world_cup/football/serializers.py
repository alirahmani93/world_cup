from rest_framework import serializers

from common.serializers import excluded_fields, BaseModelSerializer
from common.utils.time import standard_response_datetime
from .models import Match, TeamPlayer, Team, MatchResult


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


class MatchResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchResult
        exclude = excluded_fields


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


class MatchDetailSerializer(MatchSerializer):
    team_1 = TeamWithTeamPlayerSerializer()
    team_2 = TeamWithTeamPlayerSerializer()

    class Meta:
        model = Match
        exclude = excluded_fields
