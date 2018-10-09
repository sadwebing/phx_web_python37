#-_- coding: utf-8 -_-

from django.urls import path
from phxweb.customer            import DefConsumer
from phxweb.dns.dnspod_customer     import DnsDnspodRecordUpdate, DnsDnspodRecordAdd
from phxweb.dns.cloudflare_customer import DnsCloudflareRecordUpdate, DnsCloudflareRecordAdd
from phxweb.saltstack.reflesh_customer import SaltstackRefleshExecuteCdn, SaltstackRefleshExecute
from phxweb.saltstack.command_customer import SaltstackCommandDeploy, SaltstackCommandExecute
from phxweb.servers.index_customer  import ServersUpdate


channel_routing = [
    #/dns/dnspod/record
    path("^/dns/dnspod/record/update", DnsDnspodRecordUpdate),
    path("^/dns/dnspod/record/add", DnsDnspodRecordAdd),

    #/dns/cloudflare/record
    path("^/dns/cloudflare/record/update", DnsCloudflareRecordUpdate),
    path("^/dns/cloudflare/record/add", DnsCloudflareRecordAdd),

    #/saltstack/reflesh/
    path("^/saltstack/reflesh/execute/cdn", SaltstackRefleshExecuteCdn),
    path("^/saltstack/reflesh/execute", SaltstackRefleshExecute),

    #/saltstack/command/
    path("^/saltstack/command/deploy", SaltstackCommandDeploy),
    path("^/saltstack/command/execute", SaltstackCommandExecute),

    #/servers/update
    path("^/servers/update", ServersUpdate),
]