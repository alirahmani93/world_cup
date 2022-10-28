from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Configuration

excluded_fields = ['created_time', 'updated_time', 'uuid', 'is_active']


class BaseSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = None

    @classmethod
    def make_serializer(cls, queryset=None, many=True, custom_exclude_fields: list = None):
        if not queryset:
            queryset = cls.Meta.model.objects.all()
        res = cls(queryset, many=many).data
        if custom_exclude_fields:
            if many:
                for _ in res:
                    for i in custom_exclude_fields:
                        del _[i]
            else:
                for i in custom_exclude_fields:
                    del res[i]
        return res


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
