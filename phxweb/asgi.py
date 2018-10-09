"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import os
import django
from channels.routing import get_default_application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "phxweb.settings")
django.setup()
from channels.auth    import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from phxweb.routing   import channel_routing
from phxweb           import urls





application = ProtocolTypeRouter({
    # (http->django views is added by default) 
    # 普通的HTTP请求不需要我们手动在这里添加，框架会自动加载过来
    'websocket': AuthMiddlewareStack(
        URLRouter(
            channel_routing
        )
    ),
})

#application = get_default_application()
