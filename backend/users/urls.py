from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import RegisterView, MyTokenObtainPairView
from directions.views import DirectionViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'directions', DirectionViewSet, basename='direction')  # CRUD directions

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls  # ajoute les routes directions automatiquement
