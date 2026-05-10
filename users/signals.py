import logging
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_delete, post_save
from django.template.loader import render_to_string
from .models import Profile

logger = logging.getLogger(__name__)


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )

        context = {
            'user': user,
            'profile': profile,
            'site_url': settings.SITE_URL.rstrip('/') if settings.SITE_URL else '',
        }

        subject = render_to_string('users/welcome_email_subject.txt', context).strip()
        message = render_to_string('users/welcome_email.txt', context)
        html_message = render_to_string('users/welcome_email.html', context)

        email = EmailMultiAlternatives(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [profile.email],
        )
        email.attach_alternative(html_message, 'text/html')

        try:
            email.send(fail_silently=False)
        except Exception:
            logger.exception("Welcome email failed for user id %s", user.id)


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user

    if created == False and user:
        user.username = profile.username or user.username
        user.email = profile.email or ""
        user.first_name = profile.name or ""
        user.save()


def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
