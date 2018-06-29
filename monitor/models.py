# coding: utf8
from __future__ import unicode_literals

from django.db                  import models
from django.contrib.auth.models import User
from django.core                import exceptions
from phxweb.settings            import choices_prod
from detect.models              import domains
import sys
reload(sys)
sys.setdefaultencoding('utf8')

#domain_D = domains.objects.get(id=1)

choices_s = (
        (1, '启用'), 
        (0, '禁用'),
        )

class telegram_user_id_t(models.Model):
    user = models.CharField(max_length=32, null=False)
    name = models.CharField(max_length=32, null=False)
    user_id = models.IntegerField()
    class Meta:
        unique_together = ('user' ,'user_id')

    def __str__(self):
        return " | ".join([self.user, self.name, str(self.user_id)])

class minion_ip_t(models.Model):
    minion_id = models.CharField(max_length=32, null=False)
    ip_addr = models.GenericIPAddressField()
    status = models.IntegerField(choices=choices_s, default=1)
    class Meta:
        unique_together = ('minion_id' ,'ip_addr')

    def __str__(self):
        return " - ".join([self.minion_id, self.ip_addr, self.get_status_display()])

class minion_t(models.Model):
    minion_id = models.CharField(max_length=32, unique=True, null=False)
    status = models.IntegerField(choices=choices_s, default=1)

    def __str__(self):
        return " - ".join([self.minion_id, self.get_status_display()])

class project_t(models.Model):
    choices_env = (
        (1, '运营环境'), 
        (0, '测试环境'),
        )
    choices_st = (
        ('nginx',  'nginx'), 
        ('apache', 'apache'),
        ('vpn',    'vpn'),
        )
    choices_role = (
        ('main',   'main'), 
        ('backup', 'backup'),
        )
    choices_proj = (
        ('caipiao', 'caipiao'), 
        ('sport',   'sport'),
        ('houtai',   'houtai'),
        ('vpn',     'vpn'),
        )

    envir       = models.IntegerField(choices=choices_env, default=1)
    product     = models.IntegerField(choices=choices_prod)
    project     = models.CharField(max_length=10, choices=choices_proj)
    minion_id   = models.ManyToManyField(minion_t)
    server_type = models.CharField(max_length=10, choices=choices_st, default='nginx')
    role        = models.CharField(max_length=10, choices=choices_role, default='main')
    #domain      = models.ForeignKey(domains, default=domain_D.id)
    uri         = models.CharField(max_length=128, default='/')
    status      = models.IntegerField(choices=choices_s, default=1)
    info        = models.CharField(max_length=128, blank=True)
    class Meta:
        unique_together = ('product' ,'project' ,'envir', 'server_type')

    def __str__(self):
        return " - ".join([self.get_envir_display(), self.get_product_display(), self.get_project_display(), self.get_server_type_display(), self.get_status_display()])

class cdn_proj_t(models.Model):
    choices_proj = (
        (0, 'fh_app'),
        (1, 'fh_cp_static'),
        (2, 'ry_sp_static'),
        )

    project = models.IntegerField(choices=choices_proj, unique=True)
    domain  = models.ManyToManyField(domains)
    #cdn     = models.ManyToManyField(cdn_t)

    def __str__(self):
        return " - ".join([self.get_project_display()])
