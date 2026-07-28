from django.contrib import admin
from .models import Page, Service, CategorieProduit, Article, Actualite, Realisation, Contact


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['titre', 'slug', 'publie', 'date_creation', 'date_modification']
    list_filter = ['publie', 'date_creation']
    search_fields = ['titre', 'contenu']
    prepopulated_fields = {'slug': ('titre',)}
    date_hierarchy = 'date_creation'


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'ordre', 'publie']
    list_filter = ['categorie', 'publie']
    search_fields = ['nom', 'description']
    list_editable = ['ordre', 'publie']


@admin.register(CategorieProduit)
class CategorieProduitAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ordre']
    search_fields = ['nom', 'description']
    list_editable = ['ordre']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'categorie', 'prix_unitaire', 'stock', 'publie', 'date_creation']
    list_filter = ['categorie', 'publie', 'date_creation']
    search_fields = ['nom', 'description']
    list_editable = ['prix_unitaire', 'stock', 'publie']
    date_hierarchy = 'date_creation'


@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ['titre', 'date_publication', 'publie']
    list_filter = ['publie', 'date_publication']
    search_fields = ['titre', 'contenu']
    list_editable = ['publie']
    date_hierarchy = 'date_publication'


@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'client', 'date_realisation']
    list_filter = ['date_realisation']
    search_fields = ['titre', 'description', 'client']
    date_hierarchy = 'date_realisation'


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['nom', 'email', 'sujet', 'date_envoi', 'traite']
    list_filter = ['traite', 'date_envoi']
    search_fields = ['nom', 'email', 'sujet', 'message']
    list_editable = ['traite']
    date_hierarchy = 'date_envoi'
    readonly_fields = ['date_envoi']

from .models import DemandeCotation, LigneCotation, Cotation, Prestation, Facture, Paiement

class LigneCotationInline(admin.TabularInline):
    model = LigneCotation
    extra = 0

@admin.register(DemandeCotation)
class DemandeCotationAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'date_demande', 'statut']
    list_filter = ['statut', 'date_demande']
    inlines = [LigneCotationInline]

@admin.register(Cotation)
class CotationAdmin(admin.ModelAdmin):
    list_display = ['numero', 'demande', 'montant_total', 'statut', 'date_creation']
    list_filter = ['statut']

@admin.register(Prestation)
class PrestationAdmin(admin.ModelAdmin):
    list_display = ['titre', 'client', 'statut', 'montant', 'date_debut']

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['numero', 'client', 'statut', 'montant_ttc', 'date_emission']

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = ['facture', 'montant', 'mode_paiement', 'date_paiement']
