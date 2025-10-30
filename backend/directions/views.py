from rest_framework import viewsets
from .models import Direction
from .serializers import DirectionSerializer

class DirectionViewSet(viewsets.ModelViewSet):
    queryset = Direction.objects.all()
    serializer_class = DirectionSerializer
