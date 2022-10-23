from rest_framework import routers

from .views import PlayerViewSets

router = routers.DefaultRouter()
router.register('player', PlayerViewSets, basename='player')
