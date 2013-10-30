from django.db import models
from django.contrib.auth.models import User
#from string import join
from travelsite.settings import MEDIA_ROOT
#from travelsite.destinations.models import *

class Profile(models.Model):
    avatar = models.ImageField("Profile Pic", upload_to=MEDIA_ROOT, blank=True, null=True) 
    posts = models.IntegerField(default=0, blank=True, null=True)
    user = models.ForeignKey(User, unique=True)
    first_name = models.CharField(max_length=30, null=True, blank=True, default="")
    last_name = models.CharField(max_length=30, null=True, blank=True, default="")
#    hometown = models.ForeignKey(queryset=City.objects.all(), null=True, blank=True)
    hometown = models.CharField(max_length=60, null=True, blank=True, default="")
#    interests = models.ManyToManyField(queryset=Interest.objects.all(), null=True, blank=True)
#    favorite_destinations = models.ManyToManyField(queryset=Destination.objects.all(), null=True, blank=True)
    bio = models.TextField(null=True, blank=True, default="")

    def __unicode__(self):
        return self.user
