from rest_framework import routers

from .views import MatchViewSet, TeamViewSet

router = routers.DefaultRouter()
router.register('football/match', MatchViewSet, basename='football-match')
router.register('football/team', TeamViewSet, basename='football-team')
