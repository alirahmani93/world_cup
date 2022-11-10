from rest_framework import routers

from .views import MatchViewSet, TeamViewSet, MatchResultViewSet

router = routers.DefaultRouter()
router.register('football/match', MatchViewSet, basename='football-match')
router.register('football/team', TeamViewSet, basename='football-team')
router.register('football/result', MatchResultViewSet, basename='football-result')
