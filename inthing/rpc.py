from __future__ import unicode_literals
from __future__ import print_function

from threading import local

from . import urls
from . import jsonrpc


_interfaces = local()


def get_interface():
    rpc = getattr(_interfaces, 'rpc', lambda: None)()
    if rpc is None:
        rpc = jsonrpc.JSONRPC(urls.rpc_url)
    return rpc

