from django.conf import settings
from django.core.cache import cache
from django.db import connections
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from common.models import Configuration
from common.serializers import BaseSerializer, ConfigurationSerializers, HealthSerializer
from common.utils.time import standard_response_datetime, get_now


# Create your views here.

class BaseViewSet(viewsets.GenericViewSet):
    pagination_class = None

    def get_queryset(self):
        return self.queryset.filter(is_active=True)

    class Meta:
        abstract = True


class HealthViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [AllowAny]
    serializer_class = HealthSerializer

    @staticmethod
    def app():
        app = 1
        return app

    @staticmethod
    def database():
        # Postgres
        postgres = 0
        try:
            db_conn = connections['default']
            db_conn.cursor()
            postgres = 1
        except:
            print(">>>", "Postgres not available")

        if postgres:
            return 1
        else:
            return 0

    def list(self, request, *args, **kwargs):
        return Response(HealthSerializer({
            "project_name": settings.PROJECT_NAME,
            'version': settings.VERSION,
            'app': self.app(),
            'database': self.database(),
            # 'archive_database': self.archive_database(),
            # 'redis': self.redis(),
        }).data)


class ConfigurationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ConfigurationSerializers
    queryset = Configuration.objects.all()
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        """Return data what Non-sensitive information. """
        data = cache.get(f'{self.__module__}__{self.get_view_name()}')

        if data:
            data['server_time'] = standard_response_datetime(get_now())
            return Response(data=[data])

        data = self.serializer_class(Configuration.load()).data
        data['server_time'] = standard_response_datetime(get_now())

        cache.set(f'{self.__module__}__{self.get_view_name()}', data)
        return Response(data=[data])

    @action(methods=['GET'], detail=False, url_path='time', url_name='time')
    def time(self, request, *args, **kwargs):
        return Response(data={'time': standard_response_datetime(get_now())})


class DeepLinkViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = BaseSerializer
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        redirect_link = list(request.query_params)
        redirect_link = None if len(redirect_link) == 0 else redirect_link[0]
        return HttpResponse(
            f'<script>location.href="{Configuration.load().deep_link_prefix}{redirect_link}";</script>') if redirect_link else HttpResponse(
            'not found')
