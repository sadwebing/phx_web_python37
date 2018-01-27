from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class project_t(models.Model):
    envir = models.CharField(max_length=10, default='ONLINE')
    product = models.CharField(max_length=64)
    project = models.CharField(max_length=64)
    minion_id = models.CharField(max_length=32, null=True)
    server_type = models.CharField(max_length=10, default='nginx')
    role = models.CharField(max_length=16, default='main')
    domain = models.CharField(max_length=128)
    uri = models.CharField(max_length=128, null=True)
    status = models.IntegerField(default=1)
    info = models.CharField(max_length=128, null=True)
    class Meta:
        unique_together = ('product' ,'project' ,'minion_id')

    def __str__(self):
    	if self.status == 1:
    		state = 'active'
    	elif self.status == 0:
    		state = 'inactive'
    	else:
    		state = 'unknown'

    	return " - ".join([self.product, self.project, self.minion_id, state])

class minion_t(models.Model):
    minion_id = models.CharField(max_length=32, null=True)
    ip_addr = models.CharField(max_length=32, null=True)
    status = models.IntegerField(default=1)
    class Meta:
        unique_together = ('minion_id' ,'ip_addr')

    def __str__(self):
    	if self.status == 1:
    		state = 'active'
    	elif self.status == 0:
    		state = 'inactive'
    	else:
    		state = 'unknown'

    	return " - ".join([self.minion_id, self.ip_addr, state])