from __future__ import unicode_literals

from django.db import models

# Create your models here.
class tomcat_project(models.Model):
    op_time = models.CharField(max_length=20)
    op_user = models.CharField(max_length=20)
    op_salt_type = models.CharField(max_length=10)
    #op_minion_id = 
    op_jid = models.CharField(max_length=20)

class tomcat_saltstack_history(models.Model):
	op_time = models.CharField(max_length=128, blank=False)
	op_user = models.CharField(max_length=20, blank=False)
	op_ip_addr = models.GenericIPAddressField(blank=False)
	op_type = models.CharField(max_length=64, blank=False)
	op_before = models.CharField(max_length=2048, blank=False)
	op_after = models.CharField(max_length=2048, blank=False)
