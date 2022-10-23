from rest_framework import routers

from .views import ConfigurationViewSet, DeepLinkViewSet

router = routers.DefaultRouter()
router.register('common/configuration', ConfigurationViewSet, basename='configuration')
router.register('dl', DeepLinkViewSet, basename='deep-link')
