from django.dispatch import receiver
from sha_accounts.signals import user_logged_in
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from .models import ExampleProfile, ExampleRelProfile


@receiver(user_logged_in, sender=get_user_model())
def send_activation_mail(sender, user, **kwargs):
    pass


@receiver(post_save, sender=ExampleProfile)
def create_profile_rel(sender, instance, created, *args, **kwargs):
    ExampleRelProfile.objects.create(profile=instance)
