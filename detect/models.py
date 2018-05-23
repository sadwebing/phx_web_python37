# coding: utf8
from django.db import models
from phxweb.settings import choices_prod

# Create your models here.

class groups(models.Model):
    choices_s = (
                (1, '启用'), 
                (0, '禁用'),
                )

    group  = models.CharField(max_length=128, unique=True)
    client = models.CharField(max_length=12, null=False)
    method = models.CharField(max_length=12, null=False)
    ssl    = models.IntegerField(choices=choices_s, default=1)
    retry  = models.IntegerField(default=3)
    def __str__(self):
        if self.ssl == 1:
            ssl = 'ssl'
        else:
            ssl = 'nossl'
    	return " | ".join([self.group, self.client, self.method, ssl])

class domains(models.Model):
    #choices_n = (
    #            (1, 'http://'), 
    #            (0, 'https://'),
    #            )

    choices_s = (
                (1, '启用'), 
                (0, '禁用'),
                )

    #protocol = models.IntegerField(choices=choices_n, default=1) 
    name     = models.CharField(max_length=128)
    product  = models.IntegerField(choices=choices_prod)
    group    = models.ForeignKey(groups)
    content  = models.CharField(max_length=128, blank=True)
    status   = models.IntegerField(choices=choices_s, default=1)

    def __str__(self):
        if self.group.ssl == 1:
            ssl = 'ssl'
        else:
            ssl = 'nossl'
    	return " | ".join([self.get_product_display(), self.name, ' : '.join([self.group.client, self.group.method, ssl]), self.get_status_display()])