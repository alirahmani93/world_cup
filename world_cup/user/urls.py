
from rest_framework import routers

from .views import PlayerViewSets, PlayerPredictViewSet

router = routers.DefaultRouter()
router.register('player/predict', PlayerPredictViewSet, basename='player-predict')
router.register('player', PlayerViewSets, basename='player')
