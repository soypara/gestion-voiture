from rest_framework import serializers
from .models import Detenteur

class DetenteurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Detenteur
        fields = "__all__"
