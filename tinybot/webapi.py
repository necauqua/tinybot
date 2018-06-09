
import requests
import tinybot.logger as tlogger

__all__ = ('JsonRequestAPI', 'DynamicDictObject', 'NoSuchElementException', 'RequestException')

logger = tlogger.get('tinybot.webapi')


class JsonRequestAPI:
    """
    The simplest web-request API you could possibly make.
    (Well, it can be even simpler but less flexible if you remove submethods)
    """

    def __init__(self, name, link_pattern, token=None, predef_args=None):
        """
        :param name: name for User-Agent header
        :param link_pattern: URL pattern for the POST request, with {token} and {method} placeholders
        :param token: optional token which is used only to replace itself in link pattern
        :param predef_args: args which will be sent with each request, token might be stored here instead
        """
        self.link_pattern, self.token, self.predef_args = link_pattern, token, predef_args or {}
        self.session = requests.Session()
        self.session.headers['User-Agent'] = name
        self.session.headers['Accept'] = 'application/json'

    @staticmethod
    def send_request(self, method, **kwargs):
        """
        Actually sends the request with given method to be replaced in link pattern and **kwargs
        to be the JSON object sent with POST request
        """
        kwargs.update(self.predef_args)
        link = self.link_pattern.format(token=self.token or '{token}', method=method)
        logger.debug('calling method %s %s', method, kwargs)
        res = DynamicDictObject(self.session.post(link, json=kwargs).json())
        logger.debug('received answer %s', res)
        return type(self).process_result(self, res, method)

    @staticmethod
    def process_result(self, json, method):
        """
        Used to convert the result if such conversion is needed.
        RequestException can be thrown if the result is erroneous in any way
        to prevent further processing.
        """
        return json

    @staticmethod
    def close_api(self):
        """Closes the requests session, using with-construct is advised instead of this"""
        self.session.close()

    class Submethod:

        def __init__(self, api, method):
            self.api, self.method = api, method

        def __call__(self, **kwargs):
            return JsonRequestAPI.send_request(self.api, self.method, **kwargs)

        def __getattr__(self, item):
            return JsonRequestAPI.Submethod(self.api, self.method + '.' + item)

    def __getattr__(self, item):
        return JsonRequestAPI.Submethod(self, item)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        JsonRequestAPI.close_api(self)


class DynamicDictObject:
    """
    A recursive view of dict/list-like structure with __getattr__'s and __getitem__'s
    When trying to get a nonexistent item raises NoSuchElementException.
    """

    def __new__(cls, peer, path=''):
        if peer is None:
            raise NoSuchElementException(path[1:])
        if not isinstance(peer, (dict, list)):
            return peer
        return super().__new__(cls)

    def __init__(self, peer, path=None):
        self.__peer, self.__path = peer, path or ''

    @staticmethod
    def set_path(self, path):
        self.__path = '.' + path

    def __getattr__(self, item):
        peer = self.__peer
        if not isinstance(peer, dict):
            raise NoSuchElementException('Expected a dict at %s, but is was a list' % self.__path)
        return DynamicDictObject(peer.get(item), '%s.%s' % (self.__path, item))

    def __getitem__(self, item):
        child = None
        if isinstance(self.__peer, list):
            try:
                child = self.__peer[item]
            except IndexError:
                pass
        else:
            child = self.__peer.get(item)
        return DynamicDictObject(child, '%s[%s]' % (self.__path, repr(item)))

    def __contains__(self, item):
        if isinstance(self.__peer, dict):
            return item in self.__peer
        return False

    def __iter__(self):
        return map(DynamicDictObject, iter(self.__peer))

    def __repr__(self):
        return repr(self.__peer)


class RequestException(Exception):
    pass


class NoSuchElementException(Exception):
    pass
