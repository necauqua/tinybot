import asyncio
import json
from io import IOBase
from urllib.parse import urlencode

import tinybot.logger as tlogger

__all__ = ('TelegramAPI', 'BlockingTelegramAPI', 'DynamicDictObject', 'RequestException', 'NoSuchElementException')

logger = tlogger.get('tinybot.webapi')


class TelegramAPI:
    """
    The simplest web-request API for something like Telegram you could possibly make.
    """

    trace_methods = ['getUpdates']
    """
    Methods whose successful calls should not be logged.
    For example, when longpolling, the getUpdates method from Telegram API is
    called in a loop each 'timeout' seconds overfilling the log with similar
    and useless messages. 
    """

    def __init__(self, session, token):
        """
        :param session: aihttp client session to be used for making requests
        :param token: the token for the Telegram Bot API
        """
        self.__session = session
        self.__url = 'https://api.telegram.org/bot%s/' % token
        self.__file_url = 'https://api.telegram.org/file/bot%s/' % token

    async def request(self, method, **kwargs):
        """
        Send the request with given method and kwargs as JSON or URL query
        arguments (query is used when files are sent).

        If any value in kwargs at any nesting level is an instance of IOBase
        then the request is sent as multipart/form-data (and the rest of the
        args as part URL query instead of JSON body) with that value attached
        as file and it's entry in kwargs replaced by 'attach://name' as
        Telegram understands it.
        Name is either choosen sequentially (like 'file_0', 'file_1', and so
        on) or instead of a pure IOBase file parameter can be specified as a
        tuple (str, IOBase) for custom file name.
        """

        def extract_files(obj):
            fs, idx = {}, 0

            def rec(v):
                if isinstance(v, list):
                    return [rec(x) for x in v]
                if isinstance(v, dict):
                    return {k: rec(v) for k, v in v.items()}

                nonlocal fs, idx
                if isinstance(v, tuple) and len(v) == 2 and isinstance(v[1], IOBase):
                    name = str(v[0])
                    fs[name] = v[1]
                    return 'attach://' + name
                if isinstance(v, IOBase):
                    name = 'file_' + str(idx)
                    idx += 1
                    fs[name] = v
                    return 'attach://' + name
                return v

            return rec(obj), fs

        args, files = extract_files(kwargs)

        log = method not in self.trace_methods

        if log:
            logger.debug('calling method %s %s', method, args)

        if files:
            query = urlencode({k: json.dumps(v) if isinstance(v, (list, dict)) else str(v) for k, v in args.items()})
            response = await self.__session.post(self.__url + method + '?' + query, files=files)
        else:
            response = await self.__session.post(self.__url + method, json=args)

        data = DynamicDictObject(json.loads(await response.read()))

        if log:
            logger.debug('received answer %s', data)

        if 'ok' in data:
            if data.ok and 'result' in data:
                return data.result
            if 'description' in data:
                raise RequestException('server error calling \'%s\': %s' % (method, data.description))
        raise RequestException('bad response: %s' % data)

    async def download(self, file_id):
        """Small util function to get the file content from given file_id."""
        file = await self.getFile(file_id=file_id)
        return await self.__session.get(self.__file_url + file.file_path).read()

    def __getattr__(self, item):
        return TelegramAPI.Method(self, item)

    class Method:

        def __init__(self, api, method):
            self.__api = api
            self.__method = method

        def __getattr__(self, item):
            return TelegramAPI.Method(self.__api, self.__method + '.' + item)

        def __call__(self, **kwargs):
            request = self.__api.request(self.__method, **kwargs)
            request.__name__ = self.__method
            request.__qualname__ = 'TelegramAPI.' + self.__method
            return request


class BlockingTelegramAPI:

    def __init__(self, api, loop):
        self.__api = api
        self.__loop = loop

    def request(self, method, **kwargs):
        return asyncio.run_coroutine_threadsafe(self.__api.request(method, **kwargs), self.__loop).result()

    def download(self, file_id):
        return asyncio.run_coroutine_threadsafe(self.__api.download(file_id), self.__loop).result()

    def __getattr__(self, item):
        return BlockingTelegramAPI.Method(self, item)

    class Method:

        def __init__(self, api, method):
            self.__api = api
            self.__method = method

        def __getattr__(self, item):
            return BlockingTelegramAPI.Method(self.__api, self.__method + '.' + item)

        def __call__(self, **kwargs):
            return self.__api.request(self.__method, **kwargs)


class DynamicDictObject:
    """
    A recursive view of dict/list-like structure with __getattr__'s and __getitem__'s
    When trying to get a nonexistent item raises NoSuchElementException.
    """

    def __new__(cls, peer, path=''):
        if not isinstance(peer, (dict, list)):
            return peer
        return super().__new__(cls)

    def __init__(self, peer, path=''):
        self.__peer, self.__path = peer, path

    @staticmethod
    def set_path(self, path):
        self.__path = '.' + path

    def items(self):
        peer = self.__peer
        if not isinstance(peer, dict):
            raise NoSuchElementException(f'Expected an object at {self.__path[1:]}, but it was '
                                         f'\'{type(peer).__name__}\'')
        return map(lambda k: (k, self[k]), peer)

    def get(self, item):
        try:
            return self[item]
        except NoSuchElementException:
            return None

    def __getattr__(self, item):
        peer = self.__peer
        if not isinstance(peer, dict):
            raise NoSuchElementException(f'Expected an object at \'{self.__path[1:]}\', but it was '
                                         f'\'{type(peer).__name__}\'')
        path = f'{self.__path}.{item}'
        try:
            child = peer[item]
            # callables without arguments treated as properties
            # and callables with arguments are prohibited
            while callable(child):
                child = child()
        except (TypeError, KeyError):
            raise NoSuchElementException(path[1:]) from None
        return DynamicDictObject(child, path)

    def __getitem__(self, item):
        if isinstance(item, str) and item.isidentifier():
            path = f'{self.__path}.{item}'
        else:
            path = f'{self.__path}[{repr(item)}]'
        peer = self.__peer
        try:
            child = peer[item]
        except TypeError:
            raise NoSuchElementException(f'Tried to index \'{type(peer).__name__}\' at {self.__path[1:]} with key of '
                                         f'type \'{type(item).__name__}\'') from None
        except (KeyError, IndexError):
            raise NoSuchElementException(path[1:]) from None
        return DynamicDictObject(child, path)

    def __contains__(self, item):
        if isinstance(self.__peer, dict):
            return item in self.__peer
        return False

    def __iter__(self):
        if isinstance(self.__peer, list):
            path = self.__path
            return map(lambda x: DynamicDictObject(x[1], f'{path}[{x[0]}]'), enumerate(self.__peer))

        return iter(self.__peer)

    def __repr__(self):
        return repr(self.__peer)


class RequestException(Exception):
    pass


class NoSuchElementException(Exception):
    pass
