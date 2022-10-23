from django.utils.translation import gettext_lazy as _
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.response import Response

from common import statuses
from common.utils.response import custom_response
from common.views import BaseViewSet
from user.models import Player
from user.serialziers import PlayerSerializer


# Create your views here.
class PlayerViewSets(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin, BaseViewSet):
    serializer_class = PlayerSerializer
    queryset = Player.objects.filter(is_active=True)
    pagination_class = None

    def get_queryset(self):
        return self.queryset if self.request.user.is_superuser else self.queryset.filter(pk=self.request.user.pk)

    # @action(methods=["GET"], url_path='profile', url_name='profile',
    #         serializer_class=PlayerSerializer, detail=False)
    # def profile(self, *args, **kwargs):
    #     player = self.request.user.player
    #     PlayerSerializer
    #     return custom_response(data={}, status_code=statuses.OK_200)
