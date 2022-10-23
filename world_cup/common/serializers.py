from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Configuration


class BaseSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class ConfigurationSerializers(ModelSerializer):
    class Meta:
        model = Configuration
        fields = [
            'app_name', 'deep_link_prefix', 'maintenance_mode', 'app_version', 'app_version_bundle',
            'last_bundle_version', 'minimum_supported_bundle_version', 'server_time_zone', 'server_time',
            'choices_continent', 'choices_world_cup_group', 'choices_match_level', 'choices_match_status',
            'choices_winner', 'choices_team_player_role', ]


class HealthSerializer(BaseSerializer):
    project_name = serializers.CharField(max_length=256)
    version = serializers.CharField(max_length=100)
    app = serializers.BooleanField()
    database = serializers.BooleanField()
    # archive_database = serializers.BooleanField()
    # redis = serializers.BooleanField()
