from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('actualites/', views.actualites, name='actualites'),
    path('actualites/<int:actualite_id>/', views.actualite_detail, name='actualite_detail'),
    path('realisations/', views.realisations, name='realisations'),
    path('a-propos/', views.a_propos, name='a_propos'),
    path('contact/', views.contact, name='contact'),
    path('page/<slug:slug>/', views.page_detail, name='page_detail'),
    path('catalogue/', views.catalogue, name='catalogue'),
    path('catalogue/<int:cat_id>/', views.catalogue_categorie, name='catalogue_categorie'),
    path('panier/ajouter/<int:article_id>/', views.add_to_cart, name='add_to_cart'),
    path('panier/retirer/<int:article_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('demande-cotation/', views.demande_cotation, name='demande_cotation'),
    path('admin-cotations/', views.admin_demandes_list, name='admin_demandes_list'),
    path('admin-cotations/tarifer/<int:demande_id>/', views.admin_tarifer_demande, name='admin_tarifer_demande'),
    path('cotation/<int:cotation_id>/', views.cotation_detail, name='cotation_detail'),
    path('cotation/<int:cotation_id>/action/', views.cotation_action, name='cotation_action'),
    path('facture/<int:facture_id>/', views.facture_detail, name='facture_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('espace-admin/', views.admin_hub, name='admin_hub'),
    
    # Gestion Catalogue
    path('espace-admin/catalogue/', views.admin_catalogue, name='admin_catalogue'),
    path('espace-admin/catalogue/article/nouveau/', views.admin_article_form, name='admin_article_create'),
    path('espace-admin/catalogue/article/editer/<int:article_id>/', views.admin_article_form, name='admin_article_edit'),
    path('espace-admin/catalogue/categorie/nouvelle/', views.admin_categorie_form, name='admin_categorie_create'),
    path('espace-admin/catalogue/categorie/editer/<int:categorie_id>/', views.admin_categorie_form, name='admin_categorie_edit'),
]
