import zmq
import os

from zmq.auth import load_certificate


try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources


from .resources import private_keys
from .resources import public_keys


class Message(object):

    def __init__(self, *args, **kwargs):

        self.method = kwargs.get('method', None)
        self.args = kwargs.get('args', list())
        self.kwargs = kwargs.get('args', dict())


class Client(object):

    def __init__(self, *args, **kwargs):

        self.ip = kwargs.get('ip', 'tcp://localhost:8006')

        # with pkg_resources.path(private_keys, '') as r_path:
        #     private_keys_path = str(r_path)
        #     arr = os.listdir(private_keys_path)
        #     self.private_key_path = os.path.join(private_keys_path[0],
        #                                          next(x for x in arr if x.endswith(".key_secret")))
        #
        # with pkg_resources.path(public_keys, '') as r_path:
        #     private_keys_path = str(r_path)
        #     arr = os.listdir(private_keys_path)
        #     self.public_key_path = os.path.join(private_keys_path[0],
        #                                         next(x for x in arr if x.endswith(".key")))

        self.ctx = zmq.Context.instance()
        self.client = self.ctx.socket(zmq.REQ)

        # client_public, client_secret = load_certificate(self.private_key_path)
        # server_public, _ = load_certificate(self.public_key_path)
        # self.client.curve_secretkey = client_secret
        # self.client.curve_publickey = client_public
        # self.client.curve_serverkey = server_public

        self.client.connect(self.ip)
