from celery import shared_task
from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER


@shared_task
def send_mail_to(subject, message, receivers):
    send_mail(subject, message, EMAIL_HOST_USER, [receivers],
              fail_silently=False)
