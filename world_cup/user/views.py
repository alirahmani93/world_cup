from django.conf import settings
from django.core.cache import cache

from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import AllowAny, IsAuthenticated

from common import statuses
from common.choices import SMSModeKeys
from common.models import Configuration
from common.modules.sms import sms_adapter
from common.utils.response import custom_response
from common.utils.pagination import ResponsePaginator
from common.utils.time import get_now
from common.utils.utils import random_code
from common.views import BaseViewSet
from football.choices import MatchStatus
from football.models import Match
from user.models import Player, PredictionArrange
from user.serializers.serialziers import PlayerSerializer, PlayerLeaderboardSerializer, PlayerSignInMobileSerializer, \
    SignUpMobileSerializer, PredictSerializer, PlayerLogInMobileSerializer
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class PlayerViewSets(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                     BaseViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.filter(is_active=True)
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        return self.queryset if self.request.user.is_superuser else self.queryset.filter(pk=self.request.user.pk)

    @action(methods=["GET"], url_path='leaderboard', url_name='leaderboard', detail=False,
            serializer_class=PlayerLeaderboardSerializer, pagination_class=ResponsePaginator)
    def leaderboard(self, *args, **kwargs):
        data, players = cache.get('leaderboard'), None

        if not data:
            players = Player.objects.all().filter(score__gt=0).order_by('-score')
            data = self.serializer_class(players, many=True).data
            cache.set('leaderboard', data, settings.CACHE_EXPIRATION_LEADERBOARD_TIME)

        result = dict()
        result['leaderboard'] = data

        if self.request.user.is_authenticated:
            player = self.request.user.player_
            if player:
                result['rank'] = player.rank(query=players)
        return custom_response(data=result, status_code=statuses.OK_200)

    @action(
        methods=["POST"], url_path='signin/mobile', url_name='signin-mobile', detail=False,
        serializer_class=PlayerSignInMobileSerializer, pagination_class=ResponsePaginator,
        permission_classes=[AllowAny])
    def signin_mobile(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        config = Configuration.load()
        if not config.by_pass_sms:
            cached_otp = cache.get(validated_data['mobile_number'], )
            if not cached_otp:
                return custom_response(data={}, status_code=statuses.OTP_NOT_FOUND_461)
            if cached_otp != validated_data['otp']:
                return custom_response(data={}, status_code=statuses.INVALID_OTP_460)

        player, is_created = Player.objects.get_or_create(mobile_number=validated_data['mobile_number'], )
        if is_created:
            player.username = validated_data['username']
            player.is_verified = True
            player.save()
        serializer = PlayerSerializer(player)
        return custom_response(data=serializer.data, status_code=statuses.OK_200)

    @action(
        methods=["POST"], url_path='login', url_name='login', detail=False,
        serializer_class=PlayerLogInMobileSerializer, pagination_class=ResponsePaginator,
        permission_classes=[AllowAny])
    def login(self, *args, **kwargs):
        """
        Username and phone number values are asked from SSO through an api in the application and sent to the server.

        I know it's strange, but the employer wants it that way :)
        """
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        player = Player.objects.filter(username=validated_data['username'], mobile_number=validated_data['id'])
        if not player.exists():
            player = Player.objects.create(
                username=validated_data['username'],
                mobile_number=validated_data['id'],
                is_active=True,
                is_verified=True,
                profile_name=validated_data['username'],
                last_login=get_now()
            )
        else:
            player = player.first()

        if player.is_blocked:
            return custom_response(data={}, status_code=statuses.PLAYER_BLOCKED_453)

        serializer = PlayerSerializer(player)
        return custom_response(data=serializer.data, status_code=statuses.OK_200)

    @action(
        methods=["POST"], url_path='signup/mobile', url_name='signup-mobile', detail=False,
        serializer_class=SignUpMobileSerializer, pagination_class=ResponsePaginator,
        permission_classes=[AllowAny])
    def signup_mobile(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        otp = random_code(numeric=True, stringify=False, number_length=6)
        cache.set(validated_data['mobile_number'], str(otp), settings.CACHE_EXPIRATION_OTP_TIME)
        sms_adapter.send_sms(receptor=validated_data['mobile_number'], template=SMSModeKeys.SIGNUP, token=otp)

        return custom_response(data={}, status_code=statuses.OK_200)


class PlayerPredictViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                           mixins.UpdateModelMixin, BaseViewSet):
    serializer_class = PredictSerializer
    queryset = PredictionArrange.objects.filter(is_active=True)
    # pagination_class = ResponsePaginator
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["winner", "is_penalty", 'match', 'is_active']
    ordering_fields = ['is_penalty', 'created_time', 'updated_time']

    def get_queryset(self):
        return self.queryset if self.request.user.is_superuser else self.queryset.filter(player=self.request.user.pk)

    def create(self, request, *args, **kwargs):
        request.data['player'] = request.user.id
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        duration = Configuration.load().last_prediction_till_start_match_duration
        match: Match = data['match']
        if match.status != MatchStatus.NOT_STARTED or match.start_time - get_now() < duration:
            return custom_response(data={}, status_code=statuses.PREDICTION_TIME_OVER_470)

        return super(PlayerPredictViewSet, self).create(request, *args, **kwargs)
