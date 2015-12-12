from __future__ import unicode_literals
from __future__ import print_function

import os

from . import constants
from . import jsonrpc

def get_interface():
	url = os.environ.get('INTHING_URL', constants.RPC_URL)
	rpc = jsonrpc.JSONRPC(url)
	return rpc
