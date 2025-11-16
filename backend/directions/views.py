from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import Direction
from .serializers import DirectionSerializer

class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = [AllowAny]
