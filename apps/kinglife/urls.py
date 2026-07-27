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
    path('demande-cotation/', views.demande_cotation, name='demande_cotation'),
    path('cotation/<int:cotation_id>/', views.cotation_detail, name='cotation_detail'),
    path('cotation/<int:cotation_id>/action/', views.cotation_action, name='cotation_action'),
    path('facture/<int:facture_id>/', views.facture_detail, name='facture_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
