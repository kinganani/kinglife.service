from django.contrib.auth.models import User
from .models import Notification

def creer_notification(titre, message, utilisateur=None, is_for_admin=False, lien='', type_notif='info'):
    """
    Crée une notification système.
    
    :param titre: Titre court (ex: 'Nouvelle Cotation')
    :param message: Message descriptif détaillé
    :param utilisateur: Utilisateur destinataire (User instance)
    :param is_for_admin: True si c'est destiné aux administrateurs (ex: admin panel)
    :param lien: URL de redirection lors du clic (ex: '/admin-cotations/')
    :param type_notif: 'info', 'success', 'warning', ou 'error'
    """
    return Notification.objects.create(
        utilisateur=utilisateur,
        is_for_admin=is_for_admin,
        titre=titre,
        message=message,
        lien=lien,
        type_notif=type_notif
    )
