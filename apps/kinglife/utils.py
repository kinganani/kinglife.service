import json
import logging
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from .models import Notification, PushSubscription

logger = logging.getLogger(__name__)

VAPID_PUBLIC_KEY = getattr(settings, 'VAPID_PUBLIC_KEY', 'BJ4iNXUZBrhY_hjNW0gaiSGhDrYb1ARJAk-Q7ezyiyHyPeuZxtPPob-zuxeuUAhQxlqHgETkmwkN8w2Qh5kRPFk')
VAPID_PRIVATE_KEY = getattr(settings, 'VAPID_PRIVATE_KEY', '3k8z4_x_n98K2Q0X7L3j6P4b9a1c2d3e4f5g6h7i8j9')
VAPID_CLAIMS = {"sub": "mailto:kinganani20@gmail.com"}

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

def send_webpush(subscription, title, message, url='/', type_notif='info'):
    """Envoie une notification Web Push navigateur via pywebpush"""
    try:
        from pywebpush import webpush
        payload = json.dumps({
            "title": title,
            "body": message,
            "url": url,
            "type": type_notif,
            "icon": "/static/kinglife/images/logo.png",
            "badge": "/static/kinglife/images/logo.png"
        })
        subscription_info = {
            "endpoint": subscription.endpoint,
            "keys": {
                "p256dh": subscription.p256dh,
                "auth": subscription.auth
            }
        }
        webpush(
            subscription_info=subscription_info,
            data=payload,
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims=VAPID_CLAIMS,
            ttl=86400
        )
    except Exception as e:
        logger.warning(f"Note WebPush vers {subscription.endpoint[:30]}: {e}")

def creer_notification(titre, message, utilisateur=None, is_for_admin=False, lien='', type_notif='info'):
    """
    Crée une notification système et envoie une notification Web Push automatique.
    """
    notif = Notification.objects.create(
        utilisateur=utilisateur,
        is_for_admin=is_for_admin,
        titre=titre,
        message=message,
        lien=lien,
        type_notif=type_notif
    )

    try:
        subscriptions = []
        if is_for_admin:
            subscriptions = PushSubscription.objects.filter(user__is_staff=True)
            if not subscriptions.exists():
                subscriptions = PushSubscription.objects.all()
        elif utilisateur:
            subscriptions = PushSubscription.objects.filter(user=utilisateur)
        else:
            subscriptions = PushSubscription.objects.all()[:50]

        for sub in subscriptions:
            send_webpush(sub, titre, message, url=lien or '/', type_notif=type_notif)
    except Exception as err:
        logger.warning(f"Erreur envoi Push: {err}")

    return notif
