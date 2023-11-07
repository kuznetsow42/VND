from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework.routers import SimpleRouter

from users.views import EngineViewSet

router = SimpleRouter()
router.register(r"engines", EngineViewSet)

urlpatterns = [
    path('users/', include("users.urls")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc')
] + router.urls
