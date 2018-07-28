# coding: utf8
from django.db                  import models
from django.contrib.auth.models import User
from monitor.models             import project_t, project_authority_t

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
    #address = models.CharField(max_length=200,default='',blank=True)

    def __unicode__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    """Create the UserProfile when a new User is saved"""
    if created:
        profile = UserProfile()
        profile.user = instance
        profile.save()

class telegram_chat_group_t(models.Model):
    name  = models.CharField(max_length=32, null=False)
    group = models.CharField(max_length=32, null=False)
    group_id = models.IntegerField()
    class Meta:
        unique_together = ('group' ,'group_id')

    def __str__(self):
        return " | ".join([self.name, self.group, str(self.group_id)])

class telegram_user_id_t(models.Model):
    user = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=32, null=False)
    user_id = models.IntegerField()
    class Meta:
        unique_together = ('user' ,'user_id')

    def __str__(self):
        return " | ".join([self.user, self.name, str(self.user_id)])