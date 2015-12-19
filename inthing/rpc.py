from __future__ import unicode_literals
from __future__ import print_function

import os
import weakref
from threading import local

from . import constants
from . import jsonrpc


_interfaces = local()


def get_interface():
    rpc = getattr(_interfaces, 'rpc', lambda: None)()
    if rpc is None:
        #url = os.environ.get('INTHING_URL', constants.RPC_URL)
        #rpc = jsonrpc.JSONRPC(url)
        rpc = jsonrpc.WSJSONRPC()
        _interfaces.rpc = weakref.ref(rpc)
    return rpc
