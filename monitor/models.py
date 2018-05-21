# coding: utf8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.core import exceptions
from phxweb.settings import choices_prod

choices_s = (
        (1, '启用'), 
        (0, '禁用'),
        )

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
        ('nginx', 'nginx'), 
        ('apache', 'apache'),
        )
    choices_role = (
        ('main', 'main'), 
        ('backup', 'backup'),
        )
    choices_proj = (
        ('caipiao', 'caipiao'), 
        ('sport', 'sport'),
        ('cp_ht', 'cp_ht'),
        )

    envir = models.IntegerField(choices=choices_env, default=1)
    product = models.IntegerField(choices=choices_prod)
    project = models.CharField(max_length=10, choices=choices_proj)
    minion_id = models.ManyToManyField(minion_t)
    server_type = models.CharField(max_length=10, choices=choices_st, default='nginx')
    role = models.CharField(max_length=10, choices=choices_role, default='main')
    domain = models.CharField(max_length=128)
    uri = models.CharField(max_length=128, default='/')
    status = models.IntegerField(choices=choices_s, default=1)
    info = models.CharField(max_length=128, blank=True)
    class Meta:
        unique_together = ('product' ,'project' ,'envir', 'server_type')

    def __str__(self):
    	return " - ".join([self.get_envir_display(), self.get_product_display(), self.get_project_display(), self.get_server_type_display(), self.get_status_display()])
