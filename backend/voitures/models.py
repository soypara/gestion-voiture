from django.db import models

class Direction(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class EtatVoiture(models.Model):
    etat = models.CharField(max_length=50)  # ex : "En bon état", "En panne"

    def __str__(self):
        return self.etat


class Voiture(models.Model):
    matricule = models.CharField(max_length=20, unique=True)
    marque = models.CharField(max_length=100)
    modele = models.CharField(max_length=100)
    annee = models.IntegerField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)
    etat = models.ForeignKey(EtatVoiture, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.marque} {self.modele} ({self.matricule})"


class Detenteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    fonction = models.CharField(max_length=100)
    direction = models.ForeignKey(Direction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.prenom} {self.nom}"


class Detention(models.Model):
    voiture = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    detenteur = models.ForeignKey(Detenteur, on_delete=models.CASCADE)
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.detenteur} détient {self.voiture}"
