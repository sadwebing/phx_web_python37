# coding: utf8
from __future__ import unicode_literals
from django.db import models

class cf_account(models.Model):
    name = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=128, null=False)
    key = models.CharField(max_length=128, null=False)

    def __str__(self):
    	return " | ".join([self.name, self.email])

class dnspod_account(models.Model):
    name = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=128, null=False)
    key = models.CharField(max_length=128, null=False)
    
    def __str__(self):
    	return " | ".join([self.name, self.email])
        
class domain_info(models.Model):
    domain = models.CharField(max_length=128)
    route = models.CharField(max_length=32)
    cf_account_name = models.CharField(max_length=32, null=False)
    product = models.CharField(max_length=32, null=False)
    client = models.CharField(max_length=32, null=False)
    zone_id = models.CharField(max_length=256, null=False)
    record_id = models.CharField(max_length=256, null=False)
    content = models.CharField(max_length=128)
    status = models.IntegerField(default=0)
    route_status = models.IntegerField(default=0)

    class Meta:
        unique_together = ('product', 'client', 'domain', 'route')

    def __str__(self):
    	return " | ".join([self.product, self.client, self.cf_account_name, self.domain, self.route, str(self.status), str(self.route_status)])

class alter_history(models.Model):
    choices_action = (
        ('change', '修改'), 
        ('add',    '新增'),
        ('delete', '删除'),
    )

    time    = models.CharField(max_length=32, null=False)
    req_ip  = models.CharField(max_length=128, null=False)
    user    = models.CharField(max_length=32, null=False)
    pre_rec = models.CharField(max_length=256, null=False)
    now_rec = models.CharField(max_length=256, null=False)
    action  = models.CharField(max_length=10, choices=choices_action, default='change')
    status  = models.BooleanField(default=True)

    def __str__(self):
        return " | ".join([self.time, self.user, self.pre_rec, self.now_rec, self.get_action_display(), str(self.status)])