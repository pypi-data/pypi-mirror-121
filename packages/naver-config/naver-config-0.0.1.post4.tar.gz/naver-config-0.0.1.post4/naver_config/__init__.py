try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    __path__ = __import__('pkgutil').extend_path(__path__, __name__)

from .consul.consulserver import ConsulServer
from .consul.consulclient import ConsulClient
from .config.core import Core


class NaverConfig():
    def __init__(self,myApp,session):
        self.consulserver = ConsulServer() 
        self.consulclient = ConsulClient() 
        self.core = Core(myApp,session)


if __name__ == '__main__':
    pass