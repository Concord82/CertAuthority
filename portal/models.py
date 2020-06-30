from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from django.dispatch import receiver
import django_auth_ldap.backend

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(_('title'), max_length=64, blank=True)
    department = models.CharField(_('department'), max_length=64, blank=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def populate_user_profile(sender, user=None, ldap_user=None, **kwargs):
    temp_profile = None
    bucket = {}

    try:
        temp_profile = user.profile
    except:
        temp_profile = Profile.objects.create(user=user)

    bucket['title'] = ldap_user.attrs.get('title')
    bucket['department'] = ldap_user.attrs.get('department')

    for key, value in bucket.items():
        if value:
            setattr(user.profile, key, value[0].encode('utf-8'))

    user.profile.save()


django_auth_ldap.backend.populate_user.connect(populate_user_profile)
