from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DetenteurViewSet

router = DefaultRouter()
router.register(r"", DetenteurViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
