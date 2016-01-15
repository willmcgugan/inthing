from __future__ import unicode_literals
from __future__ import print_function


import os

from . import constants


inthing_url = os.environ.get('INTHING_URL', constants.RPC_URL)
rpc_url = inthing_url.rstrip('/') + '/api/public/'
event_url = inthing_url.rstrip('/') + '/api/new-event/'
