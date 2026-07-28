from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from .models import Service, Actualite, Realisation, Page, Contact, CategorieProduit, Article, DemandeCotation, LigneCotation, Cotation, Prestation, Facture, Paiement


def home(request):
    """Page d'accueil KINGLIFE SHAL U"""
    services = Service.objects.filter(publie=True)[:6]
    actualites = Actualite.objects.filter(publie=True)[:3]
    realisations = Realisation.objects.all()[:3]
    
    context = {
        'services': services,
        'actualites': actualites,
        'realisations': realisations,
    }
    return render(request, 'kinglife/home.html', context)


def services(request):
    """Page des services détaillés"""
    services = Service.objects.filter(publie=True)
    
    # Grouper par catégorie
    services_par_categorie = {}
    for service in services:
        categorie = service.get_categorie_display()
        if categorie not in services_par_categorie:
            services_par_categorie[categorie] = []
        services_par_categorie[categorie].append(service)
    
    context = {
        'services_par_categorie': services_par_categorie,
    }
    return render(request, 'kinglife/services.html', context)


def service_detail(request, service_id):
    """Détail d'un service"""
    service = get_object_or_404(Service, id=service_id, publie=True)
    return render(request, 'kinglife/service_detail.html', {'service': service})


def actualites(request):
    """Page des actualités"""
    actualites = Actualite.objects.filter(publie=True)
    return render(request, 'kinglife/actualites.html', {'actualites': actualites})


def actualite_detail(request, actualite_id):
    """Détail d'une actualité"""
    actualite = get_object_or_404(Actualite, id=actualite_id, publie=True)
    return render(request, 'kinglife/actualite_detail.html', {'actualite': actualite})


def realisations(request):
    """Page des réalisations"""
    realisations = Realisation.objects.all()
    return render(request, 'kinglife/realisations.html', {'realisations': realisations})


def a_propos(request):
    """Page À propos - Historique, Mission, Vision, Valeurs"""
    try:
        page_historique = Page.objects.get(slug='historique')
        page_mission = Page.objects.get(slug='mission')
        page_vision = Page.objects.get(slug='vision')
        page_valeurs = Page.objects.get(slug='valeurs')
    except Page.DoesNotExist:
        page_historique = None
        page_mission = None
        page_vision = None
        page_valeurs = None
    
    context = {
        'page_historique': page_historique,
        'page_mission': page_mission,
        'page_vision': page_vision,
        'page_valeurs': page_valeurs,
    }
    return render(request, 'kinglife/a_propos.html', context)


def contact(request):
    """Page de contact"""
    if request.method == 'POST':
        Contact.objects.create(
            nom=request.POST.get('nom'),
            email=request.POST.get('email'),
            telephone=request.POST.get('telephone', ''),
            sujet=request.POST.get('sujet'),
            message=request.POST.get('message')
        )
        return render(request, 'kinglife/contact_success.html')
    
    return render(request, 'kinglife/contact.html')


def page_detail(request, slug):
    """Détail d'une page statique"""
    page = get_object_or_404(Page, slug=slug, publie=True)
    return render(request, 'kinglife/page_detail.html', {'page': page})


def catalogue(request):
    """Page 1 : Grille des catégories — le client choisit sa catégorie"""
    categories = CategorieProduit.objects.annotate(
        nb_articles=Count('articles', filter=Q(articles__publie=True))
    ).filter(nb_articles__gt=0).order_by('ordre', 'nom')
    
    cart_count = len(request.session.get('cart', {}))
    
    return render(request, 'kinglife/catalogue.html', {
        'categories': categories,
        'cart_count': cart_count,
    })


def catalogue_categorie(request, cat_id):
    """Page 2 : Tableau Excel des articles d'une catégorie"""
    categorie = get_object_or_404(CategorieProduit, id=cat_id)
    toutes_categories = CategorieProduit.objects.annotate(
        nb_articles=Count('articles', filter=Q(articles__publie=True))
    ).filter(nb_articles__gt=0).order_by('ordre', 'nom')
    
    query = request.GET.get('q', '')
    articles = Article.objects.filter(publie=True, categorie=categorie)
    if query:
        articles = articles.filter(nom__icontains=query)
    
    # Cart state for this page
    cart = request.session.get('cart', {})
    cart_count = len(cart)
    cart_ids = list(cart.keys())  # which articles are already in cart
    
    return render(request, 'kinglife/catalogue_categorie.html', {
        'categorie': categorie,
        'toutes_categories': toutes_categories,
        'articles': articles,
        'query': query,
        'cart_count': cart_count,
        'cart_ids': cart_ids,
    })



@login_required
def add_to_cart(request, article_id):
    """Ajouter un article au panier — supporte AJAX, quantité personnalisée"""
    from django.http import JsonResponse
    cart = request.session.get('cart', {})
    article_id_str = str(article_id)
    
    # Support custom quantity from request
    try:
        qty = max(1, int(request.GET.get('qty', 1)))
    except (ValueError, TypeError):
        qty = 1
    
    if article_id_str not in cart:
        cart[article_id_str] = qty
    else:
        cart[article_id_str] += qty
    request.session['cart'] = cart
    
    # AJAX response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'cart_count': len(cart)})
    
    messages.success(request, 'Article ajouté au panier de cotation.')
    return redirect(request.META.get('HTTP_REFERER', 'catalogue'))

@login_required
def remove_from_cart(request, article_id):
    """Retirer un article du panier"""
    cart = request.session.get('cart', {})
    article_id_str = str(article_id)
    if article_id_str in cart:
        del cart[article_id_str]
        request.session['cart'] = cart
        messages.info(request, 'Article retiré du panier.')
    return redirect('demande_cotation')

@login_required
def demande_cotation(request):
    """Soumettre une demande de cotation (Panier)"""
    cart = request.session.get('cart', {})
    
    if request.method == 'POST':
        if not cart:
            messages.error(request, 'Votre panier est vide.')
            return redirect('catalogue')
            
        remarques = request.POST.get('remarques', '')
        demande = DemandeCotation.objects.create(
            client=request.user,
            remarques=remarques
        )
        
        # Mettre à jour les quantités avec celles du formulaire et créer les lignes
        for article_id_str in cart.keys():
            quantite = request.POST.get(f'quantite_{article_id_str}', 1)
            try:
                article = Article.objects.get(id=int(article_id_str))
                LigneCotation.objects.create(
                    demande=demande,
                    article=article,
                    quantite=int(quantite)
                )
            except Article.DoesNotExist:
                pass
                
        # Vider le panier
        request.session['cart'] = {}
        messages.success(request, 'Votre demande de cotation a été transmise avec succès. Notre équipe vous répondra avec les tarifs.')
        return redirect('dashboard')
        
    # Récupérer les articles du panier pour l'affichage (GET)
    articles_in_cart = []
    if cart:
        article_ids = [int(k) for k in cart.keys()]
        articles_qs = Article.objects.filter(id__in=article_ids)
        for art in articles_qs:
            articles_in_cart.append({
                'article': art,
                'quantite': cart[str(art.id)]
            })
            
    context = {
        'articles_in_cart': articles_in_cart,
    }
    return render(request, 'kinglife/demande_cotation.html', context)


@login_required
def cotation_detail(request, cotation_id):
    """Consulter une cotation et interagir (Accepter/Refuser)"""
    cotation = get_object_or_404(Cotation, id=cotation_id, demande__client=request.user)
    return render(request, 'kinglife/cotation_detail.html', {'cotation': cotation})


from django.contrib.admin.views.decorators import staff_member_required

@login_required
@staff_member_required
def admin_demandes_list(request):
    """Tableau de bord Admin pour voir toutes les demandes de cotation"""
    demandes_attente = DemandeCotation.objects.filter(statut='en_attente').order_by('date_demande')
    demandes_traitees = DemandeCotation.objects.exclude(statut='en_attente').order_by('-date_demande')[:50]
    
    base_template = 'kinglife/dashboard_partial.html' if request.headers.get('HX-Request') == 'true' else 'kinglife/dashboard_base.html'
    
    return render(request, 'kinglife/admin_demandes_list.html', {
        'demandes_attente': demandes_attente,
        'demandes_traitees': demandes_traitees,
        'base_template': base_template,
    })

@login_required
@staff_member_required
def admin_tarifer_demande(request, demande_id):
    """L'interface Excel-like pour que l'admin saisisse les prix"""
    demande = get_object_or_404(DemandeCotation, id=demande_id)
    lignes = demande.lignes.all()
    
    if request.method == 'POST':
        montant_sous_total = Decimal('0.00')
        
        for ligne in lignes:
            prix = request.POST.get(f'prix_{ligne.id}')
            if prix and prix.strip():
                try:
                    prix_decimal = Decimal(prix.replace(',', '.'))
                    ligne.prix_propose = prix_decimal
                    ligne.save()
                    montant_sous_total += prix_decimal * Decimal(ligne.quantite)
                except:
                    pass
                    
        # Extract discount and boat fees
        try:
            remise_pourcentage = Decimal(request.POST.get('remise', '0').replace(',', '.'))
        except:
            remise_pourcentage = Decimal('0')
            
        try:
            frais_bateau = Decimal(request.POST.get('frais_bateau', '0').replace(',', '.'))
        except:
            frais_bateau = Decimal('0')
            
        # Calculate totals
        montant_remise = montant_sous_total * (remise_pourcentage / Decimal('100'))
        montant_apres_remise = montant_sous_total - montant_remise
        montant_total = montant_apres_remise + frais_bateau
        
        # Générer la Cotation officielle
        import uuid
        numero_cotation = f"COT-{uuid.uuid4().hex[:6].upper()}"
        cotation, created = Cotation.objects.get_or_create(
            demande=demande,
            defaults={
                'numero': numero_cotation,
                'montant_sous_total': montant_sous_total,
                'remise_pourcentage': remise_pourcentage,
                'montant_remise': montant_remise,
                'montant_apres_remise': montant_apres_remise,
                'frais_bateau': frais_bateau,
                'montant_total': montant_total,
                'statut': 'envoyee'
            }
        )
        if not created:
            cotation.montant_sous_total = montant_sous_total
            cotation.remise_pourcentage = remise_pourcentage
            cotation.montant_remise = montant_remise
            cotation.montant_apres_remise = montant_apres_remise
            cotation.frais_bateau = frais_bateau
            cotation.montant_total = montant_total
            cotation.statut = 'envoyee'
            cotation.save()
            
        demande.statut = 'envoyee'
        demande.save()
        
        messages.success(request, f'Cotation {cotation.numero} générée et envoyée au client avec succès !')
        return redirect('admin_demandes_list')
        
    return render(request, 'kinglife/admin_tarifer_demande.html', {'demande': demande, 'lignes': lignes})

@login_required
@staff_member_required
def cotation_action(request, cotation_id):
    """Accepter ou refuser une cotation"""
    cotation = get_object_or_404(Cotation, id=cotation_id, demande__client=request.user)
    action = request.POST.get('action')
    
    if action == 'accepter':
        cotation.statut = 'acceptee'
        cotation.save()
        cotation.demande.statut = 'acceptee'
        cotation.demande.save()
        
        # Création automatique de la Prestation et Facture (Phase 3)
        prestation = Prestation.objects.create(
            cotation=cotation,
            client=request.user,
            titre=f"Prestation issue de Cotation {cotation.numero}",
            description=cotation.conditions or "Prestation maritime engagée",
            date_debut=cotation.date_creation.date(),
            statut='en_cours',
            montant=cotation.montant_total
        )
        
        import uuid
        num_facture = f"FAC-{cotation.numero.replace('COT-', '')}"
        Facture.objects.create(
            numero=num_facture,
            client=request.user,
            prestation=prestation,
            date_echeance=cotation.date_creation.date(),
            statut='emise',
            montant_ht=cotation.montant_total,
            montant_tva=cotation.montant_total * Decimal('0.18'),
            montant_ttc=cotation.montant_total * Decimal('1.18')
        )
        messages.success(request, 'Cotation acceptée ! La prestation et la facture correspondante ont été générées.')
    elif action == 'refuser':
        cotation.statut = 'refusee'
        cotation.save()
        cotation.demande.statut = 'refusee'
        cotation.demande.save()
        messages.info(request, 'Vous avez refusé la cotation.')
        
    return redirect('dashboard')


@login_required
def facture_detail(request, facture_id):
    """Détail de la facture imprimable avec reçu/relevé"""
    facture = get_object_or_404(Facture, id=facture_id, client=request.user)
    return render(request, 'kinglife/facture_detail.html', {'facture': facture})


def register(request):
    """Inscription d'un nouveau client"""
    from .forms import ClientRegistrationForm
    if request.method == 'POST':
        form = ClientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès.')
            return redirect('dashboard')
    else:
        form = ClientRegistrationForm()
    return render(request, 'kinglife/register.html', {'form': form})


def login_view(request):
    """Connexion utilisateur"""
    from django.contrib.auth.forms import AuthenticationForm
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Vous êtes connecté avec succès.')
            if user.is_staff or user.is_superuser:
                return redirect('admin_hub')
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'kinglife/login.html', {'form': form})


def logout_view(request):
    """Déconnexion utilisateur"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté.')
    return redirect('/')


@login_required
def dashboard(request):
    """Tableau de bord client avec historique complet"""
    from .models import DemandeCotation, Cotation, Facture, Prestation
    demandes = DemandeCotation.objects.filter(client=request.user).order_by('-date_demande')
    cotations = Cotation.objects.filter(demande__client=request.user).order_by('-date_creation')
    prestations = Prestation.objects.filter(client=request.user).order_by('-date_debut')
    factures = Facture.objects.filter(client=request.user).order_by('-date_emission')
    
    # Calcul des totaux financiers
    total_factures = sum(f.montant_ttc for f in factures if f.statut != 'annulee')
    total_paye = sum(f.montant_paye for f in factures)
    solde_du = total_factures - total_paye
    
    context = {
        'demandes': demandes,
        'cotations': cotations,
        'prestations': prestations,
        'factures': factures,
        'total_factures': total_factures,
        'total_paye': total_paye,
        'solde_du': solde_du,
    }
    return render(request, 'kinglife/dashboard.html', context)


@login_required
def admin_hub(request):
    """Hub principal de l'administration personnalisée"""
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'Accès refusé.')
        return redirect('/')
        
    from django.contrib.auth.models import User
    
    # Statistiques globales
    stats = {
        'total_clients': User.objects.filter(is_staff=False).count(),
        'demandes_attente': DemandeCotation.objects.filter(statut='en_attente').count(),
        'factures_impayees': Facture.objects.filter(statut='emise').count(),
        'articles_catalogue': Article.objects.filter(publie=True).count(),
        'services_actifs': Service.objects.filter(publie=True).count(),
        'messages_non_lus': Contact.objects.filter(traite=False).count(),
    }
    
    # Activités récentes
    activites = []
    # Demandes récentes
    recent_demandes = DemandeCotation.objects.order_by('-date_demande')[:3]
    for d in recent_demandes:
        activites.append({
            'date': d.date_demande,
            'type': 'Nouvelle demande',
            'desc': f"Demande #{d.id} de {d.client.username}",
            'url': f"/admin-cotations/tarifer/{d.id}/"
        })
    # Contacts récents
    recent_contacts = Contact.objects.order_by('-date_envoi')[:3]
    for c in recent_contacts:
        activites.append({
            'date': c.date_envoi,
            'type': 'Nouveau message',
            'desc': f"Message de {c.nom}",
            'url': "#"
        })
    
    activites.sort(key=lambda x: x['date'], reverse=True)
    
    base_template = 'kinglife/dashboard_partial.html' if request.headers.get('HX-Request') == 'true' else 'kinglife/dashboard_base.html'
    
    context = {
        'stats': stats,
        'activites': activites[:5],
        'base_template': base_template,
    }
    return render(request, 'kinglife/admin_hub.html', context)

@login_required
def admin_catalogue(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, "Accès refusé.")
        return redirect('dashboard')
        
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'delete_article':
            article_id = request.POST.get('article_id')
            Article.objects.filter(id=article_id).delete()
            messages.success(request, "Article supprimé.")
        elif action == 'delete_categorie':
            categorie_id = request.POST.get('categorie_id')
            CategorieProduit.objects.filter(id=categorie_id).delete()
            messages.success(request, "Catégorie supprimée.")
        return redirect('admin_catalogue')
            
    categories = CategorieProduit.objects.all()
    articles = Article.objects.all().select_related('categorie')
    
    base_template = 'kinglife/dashboard_partial.html' if request.headers.get('HX-Request') == 'true' else 'kinglife/dashboard_base.html'
    
    context = {
        'categories': categories,
        'articles': articles,
        'base_template': base_template,
    }
    return render(request, 'kinglife/admin_catalogue.html', context)

@login_required
def admin_article_form(request, article_id=None):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')
        
    article = None
    if article_id:
        from django.shortcuts import get_object_or_404
        article = get_object_or_404(Article, id=article_id)
        
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        categorie_id = request.POST.get('categorie')
        prix_unitaire = request.POST.get('prix_unitaire')
        unite = request.POST.get('unite')
        stock = request.POST.get('stock')
        publie = request.POST.get('publie') == 'on'
        
        categorie = CategorieProduit.objects.get(id=categorie_id)
        
        if not article:
            article = Article(nom=nom, description=description, categorie=categorie)
        else:
            article.nom = nom
            article.description = description
            article.categorie = categorie
            
        article.prix_unitaire = prix_unitaire if prix_unitaire else None
        article.unite = unite
        article.stock = stock
        article.publie = publie
        
        if 'image' in request.FILES:
            article.image = request.FILES['image']
            
        article.save()
        messages.success(request, "Article enregistré.")
        return redirect('admin_catalogue')
        
    categories = CategorieProduit.objects.all()
    base_template = 'kinglife/dashboard_partial.html' if request.headers.get('HX-Request') == 'true' else 'kinglife/dashboard_base.html'
    
    return render(request, 'kinglife/admin_article_form.html', {
        'article': article,
        'categories': categories,
        'base_template': base_template
    })

@login_required
def admin_categorie_form(request, categorie_id=None):
    if not (request.user.is_staff or request.user.is_superuser):
        return redirect('dashboard')
        
    categorie = None
    if categorie_id:
        from django.shortcuts import get_object_or_404
        categorie = get_object_or_404(CategorieProduit, id=categorie_id)
        
    if request.method == 'POST':
        nom = request.POST.get('nom')
        description = request.POST.get('description')
        ordre = request.POST.get('ordre', 0)
        
        if not categorie:
            categorie = CategorieProduit(nom=nom)
            
        categorie.nom = nom
        categorie.description = description
        categorie.ordre = ordre
        
        if 'image' in request.FILES:
            categorie.image = request.FILES['image']
            
        categorie.save()
        messages.success(request, "Catégorie enregistrée.")
        return redirect('admin_catalogue')
        
    base_template = 'kinglife/dashboard_partial.html' if request.headers.get('HX-Request') == 'true' else 'kinglife/dashboard_base.html'
    
    return render(request, 'kinglife/admin_categorie_form.html', {
        'categorie': categorie,
        'base_template': base_template
    })
