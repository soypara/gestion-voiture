from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Voiture
from .serializers import VoitureSerializer
from rest_framework.permissions import AllowAny

class VoitureViewSet(ModelViewSet):
    queryset = Voiture.objects.all().order_by('-date_ajout')
    serializer_class = VoitureSerializer
    permission_classes = [AllowAny]

class StatistiquesVoitures(APIView):
    """
    Retourne le total et le nombre par état : 'en marche', 'en panne', 'en réparation'
    """
    def get(self, request):
        total = Voiture.objects.count()
        en_marche = Voiture.objects.filter(etat="en marche").count()
        en_panne = Voiture.objects.filter(etat="en panne").count()
        en_reparation = Voiture.objects.filter(etat="en réparation").count()

        return Response({
            "total": total,
            "en_marche": en_marche,
            "en_panne": en_panne,
            "en_reparation": en_reparation
        }, status=status.HTTP_200_OK)
