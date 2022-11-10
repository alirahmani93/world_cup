from rest_framework import serializers

from common.serializers import BaseSerializer, excluded_fields
from user.models import PredictionArrange, Player


class PlayerSerializer(serializers.ModelSerializer):
    credentials = serializers.SerializerMethodField()

    class Meta:
        model = Player
        exclude = ['user_permissions', 'groups', 'token', 'password', 'is_superuser', 'is_staff']
        extra_kwargs = {
            'is_blocked': {'read_only': True},
            'is_verified': {'read_only': True},
            'is_active': {'read_only': True},
        }

    @staticmethod
    def get_credentials(obj):
        credentials = obj.get_token()
        credentials['token'] = obj.token
        return credentials


class PlayerLeaderboardSerializer(PlayerSerializer):
    class Meta:
        model = Player
        fields = ['id', 'uuid', 'score', 'profile_name', 'avatar']


class SignUpMobileSerializer(BaseSerializer):
    mobile_number = serializers.CharField()


class PlayerSignInMobileSerializer(BaseSerializer):
    mobile_number = serializers.CharField()
    otp = serializers.CharField(required=False)


class PlayerLogInMobileSerializer(BaseSerializer):
    id = serializers.CharField()
    username = serializers.CharField()


class PredictSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredictionArrange
        exclude = excluded_fields
        extra_kwargs = {
            'point': {'read_only': True},
            'is_processed': {'read_only': True},
            'is_active': {'read_only': True},
        }
