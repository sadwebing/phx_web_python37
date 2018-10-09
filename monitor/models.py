# coding: utf8
from __future__ import unicode_literals

from django.db                  import models
from django.contrib.auth.models import User
from django.core                import exceptions
from phxweb.settings            import choices_customer, choices_product, choices_permission
from detect.models              import domains, telegram_chat_group_t, telegram_user_id_t
from dns.models                 import cf_account, dnspod_account

#domain_D = domains.objects.get(id=1)
choices_st = (
        ('nginx',  'nginx'), 
        ('apache', 'apache'),
        ('mysql',  'mysql'),
        ('tomcat', 'tomcat'),
        ('nodejs', 'nodejs'),
        ('vpn',    'vpn'),
        ('flask',  'flask'),
        ('logstash', 'logstash'),
    )

choices_s = (
        (1, '启用'), 
        (0, '禁用'),
    )

choices_proj = (
        ('other',   '其他[other]'), 
        ('caipiao', '彩票[caipiao]'), 
        ('sport',   '体育[sport]'),
        ('houtai',  '后台[houtai]'),
        ('pay',     '支付[pay]'),
        ('ggz',     '广告站[ggz]'),
        ('image',   '图片[image]'),
        ('vpn',     'vpn'),
        ('httpdns', 'httpdns'),
    )

class telegram_domain_alert_t(models.Model):
    name       = models.CharField(max_length=32, null=False)
    chat_group = models.ManyToManyField(telegram_chat_group_t, blank=False)
    user_id    = models.ManyToManyField(telegram_user_id_t, blank=True)
    product    = models.IntegerField(choices=choices_product)
    customer   = models.IntegerField(choices=choices_customer, default=29)
    project    = models.CharField(max_length=10, choices=choices_proj, blank=True)
    status     = models.IntegerField(choices=choices_s, default=1)
    class Meta:
        unique_together = ('product' ,'customer')

    def __str__(self):
        return " | ".join([self.name, self.get_product_display(), self.get_customer_display(),])

class telegram_ssl_alert_t(models.Model):
    name       = models.CharField(max_length=32, null=False)
    chat_group = models.ManyToManyField(telegram_chat_group_t, blank=False)
    user_id    = models.ManyToManyField(telegram_user_id_t, blank=True)
    product    = models.IntegerField(choices=choices_product)
    customer   = models.IntegerField(choices=choices_customer, default=29)
    project    = models.CharField(max_length=10, choices=choices_proj, blank=True)
    status     = models.IntegerField(choices=choices_s, default=1)
    class Meta:
        unique_together = ('product' ,'customer')

    def __str__(self):
        return " | ".join([self.name, self.get_product_display(), self.get_customer_display(),])

class minion_ip_t(models.Model):
    minion_id = models.CharField(max_length=32, null=False)
    ip_addr = models.GenericIPAddressField()
    alive  = models.IntegerField(choices=choices_s, default=1)
    status = models.IntegerField(choices=choices_s, default=1)
    class Meta:
        unique_together = ('minion_id' ,'ip_addr')

    def __str__(self):
        return " - ".join([self.minion_id, self.ip_addr, self.get_status_display()])

class minion_t(models.Model):
    choices_provider = (
            (1, '台湾机房[taiwan]'), 
            (2, '香港机房[hongkong]'),
            (3, 'fent'),
            (4, '星联[xinglian]'),
            (5, '久速[jiusu]'),
            (6, '杜杜[dudu]'),
            (7, '网时[wangshi]'),
            (8, '优与云[youyucloud]'),
            (9, '阿里云[alicloud]'),
        )

    minion_id   = models.CharField(max_length=32, unique=True, null=False)
    system      = models.CharField(max_length=32, null=False, default='linux')
    user        = models.CharField(max_length=24, default='root')
    port        = models.IntegerField(null=False, default=11223)
    service_type = models.CharField(max_length=10, choices=choices_st, default='nginx')
    password    = models.TextField(null=False, default='/')
    price       = models.IntegerField(null=True)
    provider    = models.IntegerField(choices=choices_provider, null=False, default=1)
    alive       = models.IntegerField(choices=choices_s, default=1)
    status      = models.IntegerField(choices=choices_s, default=1)
    info        = models.TextField(blank=True)

    def __str__(self):
        return " - ".join([self.minion_id, self.get_provider_display(), self.get_status_display()])

class project_t(models.Model):
    choices_env = (
        (1, '运营环境[ONLINE]'), 
        (0, '测试环境[TEST]'),
        )
    choices_role = (
        ('main',   '主[main]'), 
        ('backup', '备[backup]'),
        )

    choices_servert = (
            ('front',   '反代服务器[front]'),
            ('backend', '后端源服务器[backend]'),
            ('other',   '其他服务器[other]'),
        )

    envir       = models.IntegerField(choices=choices_env, default=1)
    product     = models.IntegerField(choices=choices_product)
    project     = models.CharField(max_length=10, choices=choices_proj)
    customer    = models.IntegerField(choices=choices_customer, default=29)
    minion_id   = models.ManyToManyField(minion_t)
    user        = models.CharField(max_length=24, default='root')
    port        = models.IntegerField(null=False, default=11223)
    password    = models.TextField(null=False, default='/')
    server_type = models.CharField(max_length=10, choices=choices_servert, default='front')
    role        = models.CharField(max_length=10, choices=choices_role, default='main')
    #domain      = models.ForeignKey(domains, default=domain_D.id, on_delete=models.CASCADE)
    url         = models.CharField(max_length=128, default='https://arno.com')
    alive       = models.IntegerField(choices=choices_s, default=1)
    status      = models.IntegerField(choices=choices_s, default=1)
    svn         = models.IntegerField(choices=choices_s, default=0)
    privatekey  = models.TextField(null=False, default='thisisdefaultprivatekey')
    publickey   = models.TextField(null=False, default='thisisdefaultpublickey')
    info        = models.CharField(max_length=128, blank=True)
    class Meta:
        unique_together = ('product' ,'project' ,'envir', 'customer', 'server_type')

    def __str__(self):
        return " - ".join([self.get_envir_display(), self.get_product_display(), self.get_project_display(), self.get_customer_display(), self.get_server_type_display(), self.get_status_display()])

class cdn_proj_t(models.Model):
    choices_proj = (
        (0, 'APP下载专用域名'),
        (1, '凤凰彩票静态域名'),
        (3, '凤凰体育静态域名'),
        (2, '瑞银体育静态域名'),
        (4, 'JAVA彩票静态域名'),
        )

    project = models.IntegerField(choices=choices_proj, unique=True)
    domain  = models.ManyToManyField(domains)
    #cdn     = models.ManyToManyField(cdn_t)

    def __str__(self):
        return " - ".join([self.get_project_display()])

class project_authority_t(models.Model):
    name    = models.CharField(max_length=128, unique=True)
    project = models.ManyToManyField(project_t, blank=True)
    read    = models.IntegerField(choices=choices_s, default=1)
    write   = models.IntegerField(choices=choices_s, default=0)

    def __str__(self):
        return self.name +" | 读权限: "+ self.get_read_display() +" | 写权限: "+ self.get_write_display()

class dns_authority_t(models.Model):
    cf_account     = models.ForeignKey(cf_account, on_delete=models.CASCADE, blank=True, null=True)
    dnspod_account = models.ForeignKey(dnspod_account, on_delete=models.CASCADE, blank=True, null=True)
    permission     = models.CharField(max_length=10, choices=choices_permission, blank=False)

    def __str__(self):
        if self.cf_account:
            name = "CloudFlare-" + self.cf_account.name
        else:
            name = "DnsPod-" + self.dnspod_account.name
        return name + ": " + self.get_permission_display()

class permission_t(models.Model):
    permission = models.CharField(max_length=10, choices=choices_permission, blank=False, unique=True)

    def __str__(self):
        return self.get_permission_display()
