# confirmation email
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def confirmation_email_sent(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.FRONTEND_URL}/users/activate/{instance.id}/{token}"
        recipient_list = [instance.email]
        subject = 'Activate your account'
        message = f"Hello {instance.username}, \n\nPlease click the link bellow to activate your employee your account.\n Activation Link: {activation_url}"
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        except Exception as e:
            print(f'Sending email failed. Employee: {instance} \n Error is: {str(e)}')