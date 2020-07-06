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
        user_profile = Profile.objects.create(user=instance)
        user = django_auth_ldap.backend.LDAPBackend().populate_user(instance.username)
        if user:
            print(user.ldap_user.attrs)

            user_profile.title = user.ldap_user.attrs.get("title", [])[0]
            user_profile.department = user.ldap_user.attrs.get("department", [])[0]
            user_profile.save()


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


def populate_user_profile(sender, user=None, ldap_user=None, **kwargs):
    temp_profile = None
    bucket = {}

    try:
        temp_profile = user.profile

        bucket['title'] = ldap_user.attrs.get('title')
        bucket['department'] = ldap_user.attrs.get('department')

        for key, value in bucket.items():
            if value:
                setattr(user.profile, key, value[0])

        user.profile.save()
    except:
        pass


django_auth_ldap.backend.populate_user.connect(populate_user_profile)
