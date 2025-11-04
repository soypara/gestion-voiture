from django.db import models

class Direction(models.Model):
    abr = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=255)

    def __str__(self):
        return self.nom
