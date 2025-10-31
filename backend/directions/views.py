from rest_framework import viewsets
from .models import Direction
from .serializers import DirectionSerializer
from rest_framework.permissions import AllowAny


class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
    permission_classes = [AllowAny]


