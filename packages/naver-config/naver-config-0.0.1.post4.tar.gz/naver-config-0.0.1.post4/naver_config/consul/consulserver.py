from tornado.ioloop import IOLoop
from tornado.gen import coroutine
from consul.base import Timeout 
from .consulclient import ConsulClient


class ConsulServer(ConsulClient):
    def __init__(self, loop):
        self.value = None
        self.index = None
        loop.add_callback(self.watch) 

    @coroutine
    def watch(self, key): 
 
        while True:
            try:
                index, data = yield self.getValue(key, index=self.index)
                if data is not None:
                    self.value = data['Value']
                    self.index = index
            except Timeout:
                # gracefully handle request timeout
                pass


if __name__ == '__main__':
    loop = IOLoop.instance()
    _ = ConsulServer(loop)
    loop.start()
