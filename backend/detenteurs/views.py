from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import Detenteur
from .serializers import DetenteurSerializer


class DetenteurViewSet(viewsets.ModelViewSet):
    queryset = Detenteur.objects.all().order_by("nom")
    serializer_class = DetenteurSerializer
    permission_classes = [AllowAny]

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        detenteur = self.get_object()

        # voitures détenues
        voitures_detenu = detenteur.voitures_detenu.all()
        # voitures conduites
        voitures_conduites = detenteur.voitures_conduites.all()

        data = {
            "detenteur": f"{detenteur.nom} {detenteur.prenom}",

            # --- voitures détenues ---
            "voitures_detenu_ids": [v.id for v in voitures_detenu],
            "voitures_detenu_immatriculations": [
                v.immatriculation for v in voitures_detenu
            ],

            # --- voitures conduites ---
            "voitures_conduites_ids": [v.id for v in voitures_conduites],
            "voitures_conduites_immatriculations": [
                v.immatriculation for v in voitures_conduites
            ]
        }

        return Response(data)
