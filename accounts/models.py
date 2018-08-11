# coding: utf8
from django.db                  import models
from django.contrib.auth.models import User
from monitor.models             import project_authority_t, dns_authority_t, project_t, permission_t

# Create your models here.
class UserProfile(models.Model):
    choices_mg = (
                (1, '管理'), 
                (0, '普通'),
                )
    user = models.OneToOneField(User)
    role = models.CharField(max_length=200, default='', blank=True)
    manage  = models.IntegerField(choices=choices_mg, default=0)
    #project = models.ManyToManyField(project_t, blank=True)
    servers = models.ManyToManyField(project_authority_t, blank=True)
    dns     = models.ManyToManyField(dns_authority_t, blank=True)
    #address = models.CharField(max_length=200,default='',blank=True)

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    """Create the UserProfile when a new User is saved"""
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

class user_project_authority_t(models.Model):
    user       = models.OneToOneField(User, blank=False, null=False)
    project    = models.ManyToManyField(project_t, blank=False)
    permission = models.ManyToManyField(permission_t, blank=False)

    def __str__(self):
        return self.user.username
