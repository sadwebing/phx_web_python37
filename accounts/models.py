# coding: utf8
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    choices_mg = (
                (1, '管理'), 
                (0, '普通'),
                )
    user = models.OneToOneField(User)    
    role = models.CharField(max_length=200, default='', blank=True)
    manage = models.IntegerField(choices=choices_mg, default=0)
    #address = models.CharField(max_length=200,default='',blank=True)

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    """Create the UserProfile when a new User is saved"""
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

class cdn_t(models.Model):
    choices_cdn = (
        (0, 'tencent'),
        (1, 'wangsu'),
        )

    name      = models.IntegerField(choices=choices_cdn)
    account   = models.CharField(max_length=64, null=False)
    secretid  = models.CharField(max_length=128, null=False)
    secretkey = models.CharField(max_length=128, null=False)

    class Meta:
        unique_together = ('name', 'account')
    def __str__(self):
        return " | ".join([self.get_name_display(), self.account])
#post_save.connect(create_user_profile, sender=User)