from rest_framework import serializers
from .models import Direction, EtatVoiture, Voiture, Detenteur, Detention

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'


class EtatVoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = EtatVoiture
        fields = '__all__'


class VoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voiture
        fields = '__all__'


class DetenteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detenteur
        fields = '__all__'


class DetentionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detention
        fields = '__all__'
