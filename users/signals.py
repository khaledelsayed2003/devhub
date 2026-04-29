from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile
from django.core.mail import send_mail
from django.conf import settings


def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        
        subject = "Welcome to DevHub 🚀 Your developer journey starts now"

        message = """Hey there 👋

        Your DevHub profile is live — welcome aboard 🚀

        You're now part of a community where developers showcase their work, connect, and grow together.

        ✨ Next steps to stand out:
        - Complete your profile
        - Add your projects
        - Share your skills
        - Connect with other developers

        Your journey starts here — make it count 💻

        — DevHub Team
        """
        
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )


def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    
    if created == False and user:
        user.username = profile.username or user.username
        user.email = profile.email or ""
        user.first_name = profile.name or ""
        user.save()
         
# def deleteUser(sender, instance, **kwargs):
#     user = instance.user
#     user.delete()


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
# post_delete.connect(deleteUser, sender=Profile)
