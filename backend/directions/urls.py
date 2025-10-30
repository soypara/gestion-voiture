from django.urls import path
from .views import DirectionListCreateView

urlpatterns = [
    path('', DirectionListCreateView.as_view(), name='directions_list_create'),
]
