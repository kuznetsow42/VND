from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from users.views import Register, UsersReadOnly, UserDetail, EngineViewSet, StatusViewSet

router = SimpleRouter()
router.register(r"engines", EngineViewSet)
router.register(r"statuses", StatusViewSet)
router.register(r"", UsersReadOnly)


urlpatterns = [
    path("register/", Register.as_view()),
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("refresh_token/", TokenRefreshView.as_view(), name="token_refresh"),
    path("detail/", UserDetail.as_view()),
] + router.urls
