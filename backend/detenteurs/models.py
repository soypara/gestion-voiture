from django.db import models
from directions.models import Direction

class Detenteur(models.Model):

    FONCTION_CHOICES = [
        ('detenteur', 'Détenteur'),
        ('chauffeur', 'Chauffeur'),
        ('les_deux', 'Les deux'),
    ]

    photo = models.ImageField(upload_to='detenteurs_photos/', null=True, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    direction = models.ForeignKey(Direction, on_delete=models.SET_NULL, null=True)
    fonction = models.CharField(max_length=20, choices=FONCTION_CHOICES)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
