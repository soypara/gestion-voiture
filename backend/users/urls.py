from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DirectionViewSet, MyTokenObtainPairView
from .views import UserRegisterView  # à créer
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'directions', DirectionViewSet, basename='directions')

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('', include(router.urls)),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]




    

