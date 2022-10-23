from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from django.shortcuts import redirect
from django.urls import path, include
from rest_framework import routers

from common.views import HealthViewSet
from common.urls import router as common_router
from user.urls import router as user_router

router = routers.DefaultRouter()
router.register('health', HealthViewSet, basename='health')

router.registry.extend(common_router.registry)
router.registry.extend(user_router.registry)

admin.AdminSite.site_header = settings.SITE_HEADER
admin.AdminSite.site_title = settings.SITE_TITLE

urlpatterns = [
    path('', lambda request: redirect('admin/', permanent=True)),
    path('admin/', admin.site.urls),
    path('<version>/api/', include(router.urls)),
    path('api/', include(router.urls)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
