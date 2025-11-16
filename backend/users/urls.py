from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MyTokenObtainPairView
from directions.views import DirectionViewSet 
from .views import RegisterView  # à créer
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'directions', DirectionViewSet, basename='directions')

urlpatterns = [
    path('login/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]




    

