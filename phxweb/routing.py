#-_- coding: utf-8 -_-

from channels.routing    import route, route_class
from customer            import DefConsumer
from dns.dnspod_customer     import DnsDnspodRecordUpdate, DnsDnspodRecordAdd
from dns.cloudflare_customer import DnsCloudflareRecordUpdate, DnsCloudflareRecordAdd
from saltstack.reflesh_customer import SaltstackRefleshExecuteCdn, SaltstackRefleshExecute
from saltstack.command_customer import SaltstackCommandDeploy, SaltstackCommandExecute
from servers.index_customer  import ServersUpdate

channel_routing = [
    #/dns/dnspod/record
    route_class(DnsDnspodRecordUpdate, path=r"^/dns/dnspod/record/update"),
    route_class(DnsDnspodRecordAdd, path=r"^/dns/dnspod/record/add"),

    #/dns/cloudflare/record
    route_class(DnsCloudflareRecordUpdate, path=r"^/dns/cloudflare/record/update"),
    route_class(DnsCloudflareRecordAdd, path=r"^/dns/cloudflare/record/add"),

    #/saltstack/reflesh/
    route_class(SaltstackRefleshExecuteCdn, path=r"^/saltstack/reflesh/execute/cdn"),
    route_class(SaltstackRefleshExecute, path=r"^/saltstack/reflesh/execute"),

    #/saltstack/command/
    route_class(SaltstackCommandDeploy, path=r"^/saltstack/command/deploy"),
    route_class(SaltstackCommandExecute, path=r"^/saltstack/command/execute"),

    #/servers/update
    route_class(ServersUpdate, path=r"^/servers/update"),
]