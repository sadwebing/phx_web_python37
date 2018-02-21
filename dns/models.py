from __future__ import unicode_literals
from django.db import models

class cf_account(models.Model):
    name = models.CharField(max_length=32, unique=True)
    email = models.CharField(max_length=128, null=False)
    key = models.CharField(max_length=128, null=False)

    def __str__(self):
    	return " - ".join([self.name, self.email])

class domain_info(models.Model):
    domain = models.CharField(max_length=128)
    route = models.CharField(max_length=32)
    product = models.CharField(max_length=32, null=False)
    zone_id = models.CharField(max_length=256, null=False)
    record_id = models.CharField(max_length=256, null=False)
    content = models.CharField(max_length=128, unique=True)

    class Meta:
        unique_together = ('domain', 'route')

    def __str__(self):
    	return " - ".join([self.product, self.domain, self.route])