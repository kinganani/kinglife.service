from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
    """Pages du site institutionnel"""
    titre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    contenu = models.TextField()
    image = models.ImageField(upload_to='pages/', blank=True, null=True)
    publie = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['titre']
    
    def __str__(self):
        return self.titre


class Service(models.Model):
    """Services proposés par KINGLIFE SHAL U"""
    CATEGORIES = [
        ('general_trade', 'General Trade'),
        ('import_export', 'Import - Export'),
        ('ship_chandler', 'Ship Chandler'),
        ('shipping_agency', 'Shipping Agency'),
        ('transit', 'Transit'),
        ('crew_change', 'Crew Change'),
        ('offshore', 'Offshore Services'),
        ('bunker', 'Bunker Supply'),
        ('lubricant', 'Lubricant Supply'),
        ('sludge', 'Sludge Removal'),
        ('garbage', 'Garbage Removal'),
        ('maintenance', 'Shipping Maintenance'),
        ('autre', 'Autres prestations'),
    ]
    
    nom = models.CharField(max_length=200)
    categorie = models.CharField(max_length=50, choices=CATEGORIES)
    description = models.TextField()
    icone = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    ordre = models.IntegerField(default=0)
    publie = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['categorie', 'ordre', 'nom']
    
    def __str__(self):
        return f"{self.get_categorie_display()} - {self.nom}"


class CategorieProduit(models.Model):
    """Catégories de produits"""
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = "Catégorie de produit"
        verbose_name_plural = "Catégories de produits"
    
    def __str__(self):
        return self.nom


class Article(models.Model):
    """Produits et articles"""
    nom = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.ForeignKey(CategorieProduit, on_delete=models.CASCADE, related_name='articles')
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    unite = models.CharField(max_length=50, default='unité')
    image = models.ImageField(upload_to='articles/', blank=True, null=True)
    stock = models.IntegerField(default=0)
    publie = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['categorie', 'nom']
    
    def __str__(self):
        return self.nom


class Actualite(models.Model):
    """Actualités de l'entreprise"""
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    resume = models.CharField(max_length=300, blank=True)
    image = models.ImageField(upload_to='actualites/', blank=True, null=True)
    date_publication = models.DateTimeField(auto_now_add=True)
    publie = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-date_publication']
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"
    
    def __str__(self):
        return self.titre


class Realisation(models.Model):
    """Réalisations de l'entreprise"""
    titre = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='realisations/')
    date_realisation = models.DateField()
    client = models.CharField(max_length=200, blank=True)
    
    class Meta:
        ordering = ['-date_realisation']
        verbose_name = "Réalisation"
        verbose_name_plural = "Réalisations"
    
    def __str__(self):
        return self.titre


class Contact(models.Model):
    """Messages de contact"""
    nom = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.CharField(max_length=20, blank=True)
    sujet = models.CharField(max_length=200)
    message = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_envoi']
    
    def __str__(self):
        return f"{self.nom} - {self.sujet}"


class DemandeCotation(models.Model):
    """Demandes de cotation des clients"""
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de traitement'),
        ('envoyee', 'Cotation envoyée'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('annulee', 'Annulée'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='demandes_cotation')
    date_demande = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    remarques = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date_demande']
        verbose_name = "Demande de cotation"
        verbose_name_plural = "Demandes de cotations"
    
    def __str__(self):
        return f"Demande #{self.id} - {self.client.username}"


class LigneCotation(models.Model):
    """Lignes d'une demande de cotation"""
    demande = models.ForeignKey(DemandeCotation, on_delete=models.CASCADE, related_name='lignes')
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantite = models.IntegerField()
    prix_propose = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    remarques = models.TextField(blank=True)
    
    class Meta:
        verbose_name = "Ligne de cotation"
        verbose_name_plural = "Lignes de cotations"
    
    def __str__(self):
        return f"{self.article.nom} x {self.quantite}"


class Cotation(models.Model):
    """Cotations officielles"""
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('envoyee', 'Envoyée'),
        ('acceptee', 'Acceptée'),
        ('refusee', 'Refusée'),
        ('expiree', 'Expirée'),
    ]
    
    demande = models.OneToOneField(DemandeCotation, on_delete=models.CASCADE, related_name='cotation')
    numero = models.CharField(max_length=50, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_envoi = models.DateTimeField(null=True, blank=True)
    date_validite = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='brouillon')
    
    # Financial details
    montant_sous_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    remise_pourcentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    montant_remise = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    montant_apres_remise = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    frais_bateau = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    montant_total = models.DecimalField(max_digits=12, decimal_places=2) # GRAND TOTAL
    
    conditions = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date_creation']
    
    def __str__(self):
        return f"Cotation {self.numero}"


class Prestation(models.Model):
    """Prestations réalisées"""
    STATUT_CHOICES = [
        ('planifiee', 'Planifiée'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('facturee', 'Facturée'),
        ('annulee', 'Annulée'),
    ]
    
    cotation = models.ForeignKey(Cotation, on_delete=models.CASCADE, related_name='prestations', null=True, blank=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='prestations')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='planifiee')
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    
    class Meta:
        ordering = ['-date_debut']
    
    def __str__(self):
        return f"{self.titre} - {self.client.username}"


class Facture(models.Model):
    """Factures"""
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('emise', 'Émise'),
        ('payee', 'Payée'),
        ('partiellement_payee', 'Partiellement payée'),
        ('annulee', 'Annulée'),
    ]
    
    numero = models.CharField(max_length=50, unique=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='factures')
    prestation = models.ForeignKey(Prestation, on_delete=models.CASCADE, related_name='factures', null=True, blank=True)
    date_emission = models.DateTimeField(auto_now_add=True)
    date_echeance = models.DateField()
    statut = models.CharField(max_length=25, choices=STATUT_CHOICES, default='brouillon')
    montant_ht = models.DecimalField(max_digits=12, decimal_places=2)
    montant_tva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    montant_ttc = models.DecimalField(max_digits=12, decimal_places=2)
    montant_paye = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    regroupement = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='factures_regroupees')
    
    class Meta:
        ordering = ['-date_emission']
    
    def __str__(self):
        return f"Facture {self.numero}"


class Paiement(models.Model):
    """Paiements"""
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='paiements')
    date_paiement = models.DateTimeField(auto_now_add=True)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    mode_paiement = models.CharField(max_length=50)
    reference = models.CharField(max_length=100, blank=True)
    
    class Meta:
        ordering = ['-date_paiement']
    
    def __str__(self):
        return f"Paiement {self.montant}€ - {self.facture.numero}"
