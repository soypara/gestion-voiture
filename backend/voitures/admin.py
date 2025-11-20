from django.contrib import admin
from .models import Voiture

@admin.register(Voiture)
class VoitureAdmin(admin.ModelAdmin):
    list_display = (
        'immatriculation',
        'marque',       # remplace 'description'
        'direction',
        'detenteur',
        'chauffeur',
        'origine',
        'etat',
        'livret',
        'carte_grise',
        'date_ajout',
    )
    list_filter = ('etat', 'direction')
    search_fields = ('immatriculation', 'marque', 'direction', 'detenteur', 'chauffeur')
