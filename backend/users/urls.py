from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),      # Inscription
    path('login/', TokenObtainPairView.as_view(), name='login'),      # Connexion JWT
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Refresh token
]
