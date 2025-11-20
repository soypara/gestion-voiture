from rest_framework import serializers
from .models import Voiture

class VoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voiture
        fields = [
            "id",
            "immatriculation",
            "marque",
            "direction",
            "detenteur",
            "chauffeur",
            "origine",
            "etat",
            "observation",
            "livret",
            "carte_grise",
            "date_ajout",
        ]
