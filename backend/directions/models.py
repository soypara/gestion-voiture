from django.db import models

class Direction(models.Model):
    abr = models.CharField(max_length=100)
    nom = models.TextField(blank=True)

    def __str__(self):
        return self.nom
