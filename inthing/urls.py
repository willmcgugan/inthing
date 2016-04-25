"""URLs for inthing.io."""

from __future__ import print_function
from __future__ import unicode_literals

import os

from . import constants


# URL Inthing server, May be overriden by INTHING_URL env variable
inthing_url = os.environ.get('INTHING_URL', constants.RPC_URL)
# URL of JSONRPC
rpc_url = inthing_url.rstrip('/') + '/api/public/'
# URL where events are posted
event_url = inthing_url.rstrip('/') + '/api/new-event/'
