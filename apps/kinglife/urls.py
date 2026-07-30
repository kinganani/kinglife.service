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
    path('google-login/', views.google_login_api, name='google_login_api'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('espace-admin/', views.admin_hub, name='admin_hub'),
    path('notifications/marquer-lues/', views.marquer_notifications_lues, name='marquer_notifications_lues'),
    path('api/notifications/list/', views.get_notifications_api, name='get_notifications_api'),
    path('api/notifications/quick-reply/', views.quick_reply_api, name='quick_reply_api'),
    path('api/push/subscribe/', views.push_subscribe, name='push_subscribe'),
    path('api/push/test/', views.push_test_notification, name='push_test_notification'),
    path('offline/', views.offline_view, name='offline'),
    
    # Gestion Messages Admin
    path('espace-admin/messages/', views.admin_messages, name='admin_messages'),
    path('espace-admin/messages/<int:msg_id>/', views.admin_message_detail, name='admin_message_detail'),
    path('espace-admin/messages/<int:msg_id>/repondre/', views.admin_message_reply, name='admin_message_reply'),
    
    # Gestion Catalogue
    path('espace-admin/catalogue/', views.admin_catalogue, name='admin_catalogue'),
    path('espace-admin/catalogue/article/nouveau/', views.admin_article_form, name='admin_article_create'),
    path('espace-admin/catalogue/article/editer/<int:article_id>/', views.admin_article_form, name='admin_article_edit'),
    path('espace-admin/catalogue/categorie/nouvelle/', views.admin_categorie_form, name='admin_categorie_create'),
    path('espace-admin/catalogue/categorie/editer/<int:categorie_id>/', views.admin_categorie_form, name='admin_categorie_edit'),
    
    # Gestion Services
    path('espace-admin/services/', views.admin_services, name='admin_services'),
    path('espace-admin/services/nouveau/', views.admin_service_form, name='admin_service_create'),
    path('espace-admin/services/editer/<int:service_id>/', views.admin_service_form, name='admin_service_edit'),
    path('espace-admin/services/supprimer/<int:service_id>/', views.admin_service_delete, name='admin_service_delete'),
    
    # Gestion Actualités
    path('espace-admin/actualites/', views.admin_actualites, name='admin_actualites'),
    path('espace-admin/actualites/nouvelle/', views.admin_actualite_form, name='admin_actualite_create'),
    path('espace-admin/actualites/editer/<int:actualite_id>/', views.admin_actualite_form, name='admin_actualite_edit'),
    path('espace-admin/actualites/supprimer/<int:actualite_id>/', views.admin_actualite_delete, name='admin_actualite_delete'),
    
    # Gestion Réalisations
    path('espace-admin/realisations/', views.admin_realisations, name='admin_realisations'),
    path('espace-admin/realisations/nouvelle/', views.admin_realisation_form, name='admin_realisation_create'),
    path('espace-admin/realisations/editer/<int:realisation_id>/', views.admin_realisation_form, name='admin_realisation_edit'),
    path('espace-admin/realisations/supprimer/<int:realisation_id>/', views.admin_realisation_delete, name='admin_realisation_delete'),

    # Gestion Factures
    path('espace-admin/factures/', views.admin_factures, name='admin_factures'),
    path('espace-admin/factures/<int:facture_id>/', views.admin_facture_detail, name='admin_facture_detail'),
    path('espace-admin/factures/<int:facture_id>/paiement/', views.admin_facture_paiement, name='admin_facture_paiement'),
    path('espace-admin/factures/<int:facture_id>/achats/', views.admin_facture_liste_achats, name='admin_facture_liste_achats'),
    
    # Comptabilité / Soldes
    path('espace-admin/comptabilite/soldes/', views.admin_soldes_clients, name='admin_soldes_clients'),
]
