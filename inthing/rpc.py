from __future__ import print_function
from __future__ import unicode_literals

from . import urls
from . import jsonrpc


def get_interface():
    """Get remote interface to Inthing."""
    return jsonrpc.JSONRPC(urls.rpc_url)
