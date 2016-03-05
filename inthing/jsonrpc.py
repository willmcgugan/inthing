from __future__ import unicode_literals
from __future__ import print_function

import json

import requests



class ProtocolError(Exception):
    """Errors where the server didn't return the correct response"""


class JSONRPCError(Exception):
    """Base class for exceptions returned from the server"""
    def __init__(self, method, code, data, message):
        self.method = method
        self.code = code
        self.data = data
        self.message = message
        super(JSONRPCError, self).__init__(message)


class RemoteError(JSONRPCError):
    """One of the generic error types defined in ErrorCode"""


class RemoteMethodError(JSONRPCError):
    """An error returned from the server"""


class ErrorCode(object):
    """Enumeration of JSONRPC error codes"""

    parse_error = -32700
    invalid_request = -32600
    method_not_found = -32601
    invalid_params = -32602
    internal_error = -32603

    to_str = {-32700: "Parse error",
              -32600: "Invalid Request",
              -32601: "Method not found",
              -32602: "Invalid params",
              -32603: "Internal error"}


class Batch(object):
    """An object that stores a batch of rpc calls

    May be used as a context manager

        with client.batch() as batch:
            batch.call("method1", foo="bar")
            batch.call("method2", foo="baz")

    Method call results are stored in `results` which maps the call id on to results.
    Errors are contained in `errors` which maps the call id on to a dictionary with error code / message

    """

    def __init__(self, client):
        self.client = client
        self.calls = []
        self.sent = False
        self.responses = None
        self.errors = None
        self.results = None
        self.ids_used = set()
        self.methods = {}
        super(Batch, self).__init__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if not exc_type:
            self.send()

    def call(self, method, **params):
        """Add a call to the batch, using a default id"""
        call = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": self.client.new_call_id()
        }
        self.calls.append(call)
        self.methods[call['id']] = method

    def call_with_id(self, call_id, method, **params):
        """Add a call to the batch with a supplied id"""
        if call_id in self.ids_used:
            raise ValueError("duplicate call id in batch")
        call = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": call_id
        }
        self.calls.append(call)
        self.ids_used.add(call_id)
        self.methods[call['id']] = method

    def notify(self, method, **params):
        call = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
        }
        self.calls.append(call)

    def send(self):
        response_json = self.client._send(self.calls)
        self.sent = True
        response = json.loads(response_json)

        if not isinstance(response, list):
            raise ProtocolError("Expected a list of response from the server")

        self.responses = [(r.get('error', None), r.get('result', None))
                          for r in response]
        self.errors = {r['id']: r['error'] for r in response if 'error' in r}
        self.results = {r['id']: r for r in response if 'id' in r and 'error' not in r}

    def get_result(self, call_id, default=Ellipsis):
        """Get a result from the batch, potentially raising rpc errors"""
        if call_id in self.results:
            return self.results[call_id].get('result', None)
        elif call_id in self.errors:
            if default is Ellipsis:
                self.client._handle_error(self.methods[call_id], self.errors[call_id])
            else:
                return default
        else:
            raise KeyError("No such call_id in response")


class JSONRPC(object):
    """A client for a JSONRPC server"""

    unknown_error_msg = "the server did not supply further information"

    def __init__(self, url, ssl_verify=True):
        self.url = url
        self.call_id = 1
        self.ssl_verify = ssl_verify

    def new_call_id(self):
        self.call_id += 1
        return self.call_id

    def _send(self, call):
        call_json = json.dumps(call).encode('utf-8')
        response_json = requests.post(self.url, call_json, verify=self.ssl_verify).json()
        return response_json

    def call(self, method, **params):
        """Call a remote method"""
        call_id = self.new_call_id()
        call = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": call_id
        }
        response = self._send(call)

        if 'jsonrpc' not in response or 'id' not in response:
            raise ProtocolError("Invalid response from server")

        if response['jsonrpc'] != '2.0':
            raise ProtocolError("Client only understands JSONRPC v2.0")

        if response['id'] != call_id:
            raise ProtocolError("Invalid response from the server, 'id' field does not match")

        if 'error' in response:
            error = response['error']
            self._handle_error(method, error)

        return response.get('result', None)

    def notify(self, method, **params):
        """Send a notification to the server"""
        notify = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params
        }
        self._send(notify)

    def batch(self):
        """Create a batch object that can be used to send multiple calls / notifications"""
        return Batch(self)

    def _handle_error(self, method, error):
        code = error.get('code')
        if code in ErrorCode.to_str:
            raise RemoteError(method,
                              code,
                              error.get('data', None),
                              error.get('message', ErrorCode.to_str[code]))
        raise RemoteMethodError(method,
                                code,
                                error.get('data', None),
                                error.get('message', self.unknown_error_msg))


# class WSJSONRPC(JSONRPC):
#     """An interface to an JSONRPC server proxied over a websocket"""

#     def __init__(self, api_url="ws://127.0.0.1:7474/api/"):
#         self.api_url = api_url
#         self.call_id = 0
#         self.ws = websocket.create_connection(self.api_url)

#     def on_close(self):
#         pass

#     def _send(self, call):
#         call_json = json.dumps(call)
#         self.ws.send(call_json)
#         response_json = self.ws.recv()
#         response = json.loads(response_json)
#         return response
