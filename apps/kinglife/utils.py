from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Notification

def send_html_email(subject, template_name, context, recipient_list):
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=recipient_list
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send(fail_silently=True)

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
