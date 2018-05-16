from django.db import models

# Create your models here.

class groups(models.Model):
    group  = models.CharField(max_length=128, unique=True)
    client = models.CharField(max_length=12, null=False)
    method = models.CharField(max_length=12, null=False)
    ssl    = models.IntegerField(default=1)
    def __str__(self):
        if self.ssl == 1:
            ssl = 'ssl'
        else:
            ssl = 'nossl'
    	return " | ".join([self.group, self.client, self.method, ssl])

class domains(models.Model):

    prod_choices = ( 
                (0, 'pub'),
                (1, 'ali'), 
                (2, 'guangda'), 
                (3, 'leying'), 
                (4, 'caitou'), 
                (5, 'tiantian'), 
                (6, 'sande'), 
                (7, 'uc'), 
                (8, '9393'), 
                (9, '3535'), 
                (10, 'agcai'), 
                (11, 'wanyou'),
                )

    name  = models.CharField(max_length=128)
    product = models.IntegerField(choices=prod_choices)
    group   = models.ForeignKey(groups)
    content = models.CharField(max_length=128, blank=True)
    status  = models.IntegerField(default=1)

    def __str__(self):
        if self.group.ssl == 1:
            ssl = 'ssl'
        else:
            ssl = 'nossl'
    	return " | ".join([self.get_product_display(), self.name, ' : '.join([self.group.client, self.group.method, ssl])])