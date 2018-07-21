from django.db import models

# Create your models here.
class rsa_key_t(models.Model):
    name = models.CharField(max_length=32, null=False, unique=True)
    privatekey = models.TextField(null=False)
    publickey  = models.TextField(null=False)

    def __str__(self):
        return self.name