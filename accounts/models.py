from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)    
    role = models.CharField(max_length=200, default='', blank=True)
    #address = models.CharField(max_length=200,default='',blank=True)

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    """Create the UserProfile when a new User is saved"""
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

#post_save.connect(create_user_profile, sender=User)