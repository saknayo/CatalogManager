from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator

class Profile(models.Model):
    user       = models.OneToOneField(User, on_delete=models.CASCADE)
    user_level = models.IntegerField(default=-1,validators=[MaxValueValidator(7),MinValueValidator(-1)])
    gender     = models.TextField(max_length=500, blank=True)
    company    = models.TextField(max_length=500, blank=True)
    location   = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    url        = models.TextField(max_length=500, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try :
        instance.profile.save()
    except ObjectDoesNotExist:
        Profile.objects.create(user=instance)
