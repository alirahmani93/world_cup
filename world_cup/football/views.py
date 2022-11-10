from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny

from common import statuses
from common.utils.response import custom_response
from common.utils.time import get_now
from common.views import BaseViewSet
from .models import Match, Team, MatchResult
from .serializers import MatchSerializer, TeamSerializer, TeamWithTeamPlayerSerializer, MatchResultSerializer, \
    MatchDetailSerializer


class MatchViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = Match.objects.filter(is_active=True)
    serializer_class = MatchSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["end_time", "start_time", 'level', 'status']
    ordering_fields = ['start_time', ]
    serializer_classes = {
        'retrieve': MatchDetailSerializer
    }

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        return self.serializer_class


class TeamViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = Team.objects.filter(is_active=True)
    serializer_class = TeamSerializer

    def get_serializer_class(self):
        if self.request.query_params.get('with_player'):
            return TeamWithTeamPlayerSerializer
        return self.serializer_class

    @action(
        methods=["GET"], url_path='temp', url_name='temp', detail=False,
        permission_classes=[AllowAny])
    def temp(self, *args, **kwargs):
        from .tasks import calculate
        t1 = get_now()
        calculate(match=Match.objects.last())
        print('\x1b[0;31;40m calculation time: ', get_now() - t1, )
        return custom_response(data={}, status_code=statuses.OK_200)


class MatchResultViewSet(ListModelMixin, RetrieveModelMixin, BaseViewSet):
    queryset = MatchResult.objects.filter(is_active=True)
    serializer_class = MatchResultSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["match", "winner", 'is_penalty', 'is_processed']
    ordering_fields = ['created_time', 'is_processed', 'is_penalty']
