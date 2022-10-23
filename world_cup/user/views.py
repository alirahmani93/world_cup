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
from user.models import Player, PredictionArrange
from user.serializers.serialziers import PlayerSerializer, PlayerLeaderboardSerializer, PlayerSignInMobileSerializer, \
    SignUpMobileSerializer, PredictSerializer
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class PlayerViewSets(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, BaseViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.filter(is_active=True)
    pagination_class = ResponsePaginator
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        return self.queryset if self.request.user.is_superuser else self.queryset.filter(pk=self.request.user.pk)

    @action(methods=["GET"], url_path='leaderboard', url_name='leaderboard', detail=False,
            serializer_class=PlayerLeaderboardSerializer, pagination_class=ResponsePaginator)
    def leaderboard(self, *args, **kwargs):
        data = cache.get('leaderboard')
        if not data:
            players = Player.objects.all().order_by('score')
            data = self.serializer_class(players, many=True).data
            cache.set('leaderboard', data, settings.CACHE_EXPIRATION_LEADERBOARD_TIME)
        return custom_response(data=data, status_code=statuses.OK_200)

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
            player.is_verified = player.is_verified
            player.save()
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
        print(otp)
        cache.set(validated_data['mobile_number'], str(otp), settings.CACHE_EXPIRATION_OTP_TIME)
        sms_adapter.send_sms(receptor=validated_data['mobile_number'], template=SMSModeKeys.SIGNUP, token=otp)

        return custom_response(data={}, status_code=statuses.OK_200)

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
            player.is_verified = player.is_verified
            player.save()
        serializer = PlayerSerializer(player)

        return custom_response(data=serializer.data, status_code=statuses.OK_200)


class PlayerPredictViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin,
                           mixins.UpdateModelMixin, BaseViewSet):
    serializer_class = PredictSerializer
    queryset = PredictionArrange.objects.filter(is_active=True)
    pagination_class = ResponsePaginator
    permission_classes = [IsAuthenticated, ]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["winner", "is_penalty", 'match', 'is_active']
    ordering_fields = ['is_penalty', 'created_time', 'updated_time']

    def get_queryset(self):
        return self.queryset if self.request.user.is_superuser else self.queryset.filter(player=self.request.user.pk)

