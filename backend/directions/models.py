from django.db import models

class Direction(models.Model):
    abr = models.CharField(max_length=10)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

