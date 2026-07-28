from .models import Notification

def notifications(request):
    """
    Rend les notifications non lues disponibles dans tous les templates
    pour l'utilisateur connecté.
    """
    if not request.user.is_authenticated:
        return {'unread_notifications': [], 'unread_notifications_count': 0}
        
    if request.user.is_staff or request.user.is_superuser:
        # Pour les admins : récupérer les notifications admin + notifications personnelles
        notifs = Notification.objects.filter(lue=False).filter(
            is_for_admin=True
        ) | Notification.objects.filter(lue=False, utilisateur=request.user)
    else:
        # Pour les clients : uniquement leurs notifications personnelles
        notifs = Notification.objects.filter(lue=False, utilisateur=request.user)
        
    notifs = notifs.order_by('-date_creation')[:10] # Garder les 10 plus récentes
    count = notifs.count()
    
    return {
        'unread_notifications': notifs,
        'unread_notifications_count': count
    }
