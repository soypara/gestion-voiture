from django.db import models
from detenteurs.models import Detenteur   # <-- adapte le chemin selon ton app !

class Voiture(models.Model):
    ETATS = [
        ("bon etat", "Bon état"),
        ("moyen", "Moyen"),
        ("en panne", "En panne"),
    ]

    LIVRET_CHOICES = [
        ("fait", "Fait"),
        ("non fait", "Non fait"),
        ("SLM", "SLM"),
    ]

    CARTE_GR_CHOICES = [
        ("Carte Grise", "Carte Grise"),
        ("SCG", "SCG"),
        ("Carte rose", "Carte rose"),
        ("Carte rose(CG en cours)", "Carte rose (CG en cours)"),
        ("attestation", "Attestation"),
        ("lieux", "Lieux"),
    ]

    immatriculation = models.CharField(max_length=50, unique=True)
    marque = models.CharField(max_length=100, default="MNDPT")

    # vient de la liste des directions (Direction model ou string ?)
    direction = models.CharField(max_length=100, default="")

    origine = models.CharField(max_length=100, blank=True)
    etat = models.CharField(max_length=20, choices=ETATS, default="bon etat")
    observation = models.TextField(blank=True)

    livret = models.CharField(max_length=20, choices=LIVRET_CHOICES, default="non fait")
    carte_grise = models.CharField(max_length=50, choices=CARTE_GR_CHOICES, default="Carte Grise")

    date_ajout = models.DateTimeField(auto_now_add=True)

    # --- Relations ---
    detenteur = models.ForeignKey(
        Detenteur,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="voitures_detenu"
    )

    chauffeur = models.ForeignKey(
        Detenteur,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name="voitures_conduites"
    )

    def __str__(self):
        return f"{self.immatriculation} — {self.marque}"
