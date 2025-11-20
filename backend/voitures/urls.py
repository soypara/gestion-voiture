from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import VoitureViewSet, StatistiquesVoitures

router = DefaultRouter()
router.register(r'voitures', VoitureViewSet, basename='voiture')

urlpatterns = [
    path('voitures/stats/', StatistiquesVoitures.as_view(), name='voitures-stats'),
]

urlpatterns += router.urls
