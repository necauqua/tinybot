import asyncio
import json
from asyncio import run_coroutine_threadsafe
from datetime import datetime, timedelta
from io import IOBase
from traceback import print_exc

from aiohttp import MultipartWriter

import tinybot.logger as tlogger

__all__ = (
    'TelegramAPI', 'BlockingTelegramAPI', 'DynamicDictObject',
    'RequestError', 'NoSuchElementError', 'DynamicTypeError'
)

logger = tlogger.get('tinybot.webapi')


class Submethods:

    def call(self, method, *args, **kwargs):
        pass

    def __getattr__(self, item):
        return Submethods.Method(self, item)

    class Method:

        def __init__(self, base, method):
            self.__base = base
            self.__method = method

        def __getattr__(self, item):
            return Submethods.Method(self.__base, self.__method + '.' + item)

        def __call__(self, *args, **kwargs):
            return self.__base.call(self.__method, *args, **kwargs)


class TelegramAPI(Submethods):
    """
    Very simple async web-request Python binding to the Telegram Bot API.
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
        self.__token = token
        self.__url = 'https://api.telegram.org/bot%s/' % token
        self.__file_url = 'https://api.telegram.org/file/bot%s/' % token
        self.__file_link_cache = {}

    def request(self, method, **kwargs):
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

        async def coroutine():
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
                        return f'attach://{name}'
                    if isinstance(v, IOBase):
                        name = f'file_{idx}'
                        idx += 1
                        fs[name] = v
                        return f'attach://{name}'
                    return v

                return rec(obj), fs

            args, files = extract_files(kwargs)

            log = method not in self.trace_methods

            if log:
                logger.debug(f'calling method {method} {args}')

            if files:
                params = {k: json.dumps(v) if isinstance(v, (list, dict)) else str(v) for k, v in args.items()}

                writer = MultipartWriter('form-data')
                for n, file in files.items():
                    writer.append(file).set_content_disposition('form-data', filename=n, name=n)

                response = await self.__session.post(self.__url + method, params=params, data=writer)
            else:
                response = await self.__session.post(self.__url + method, json=args)

            data = DynamicDictObject(await response.json())

            if log:
                logger.debug(f'received answer {data}')

            if 'ok' in data:
                if data.ok and 'result' in data:
                    return data.result
                if 'description' in data:
                    raise RequestError(f'server error calling \'{method}\': {data.description}')
            raise RequestError(f'bad response: {data}')

        c = coroutine()
        c.__name__ = method
        c.__qualname__ = f'TelegramAPI.{method}'
        return c

    call = request

    class SafeWrapper(Submethods):
        """
        This is a wrapper around the request method, that catches any errors and retries the request
        until provided limit of consecutive errors is reached. Those errors are logged.
        """

        def __init__(self, api, retries):
            self.__api = api
            self.__retries = retries

        async def call(self, method, *args, **kwargs):
            retries = self.__retries
            api = self.__api
            tries = 0
            while True:
                try:
                    tries += 1
                    return await api.request(method, **kwargs)
                except:
                    if tries >= retries:
                        logger.error(f'{method} call failed {retries} time{retries == 1 and "" or "s"}')
                        raise
                    else:
                        logger.warning(f'{method} call failed, retry #{tries} in 1 second...')
                        print_exc()
                        await asyncio.sleep(1)

    def safe(self, retries=5):
        return TelegramAPI.SafeWrapper(self, retries) if retries > 1 else self

    async def get_file_cached(self, file_id):
        """
        This is a cached version of the getFile API call.
        Telegram servers `guarantee <https://core.telegram.org/bots/api#getfile>`_
        that the link they provide is valid for at least one hour, so we cache the links for that one hour.
        This method is recommended to use when your bot deals with a lot of file work.
        """
        entry = self.__file_link_cache.get(file_id)
        now = datetime.utcnow()

        if entry is not None and entry[0] < now:
            return entry[1]

        request_coroutine = self.getFile(file_id=file_id)

        # and while the real request is processed we cleanup old entries, idk how ok this is
        self.__file_link_cache = {k: v for k, v in self.__file_link_cache.items() if v[0] >= now}

        file = await request_coroutine
        self.__file_link_cache[file_id] = (now + timedelta(hours=1), file)
        return file

    async def download(self, file_id):
        """
        A util function to download the file from identified by given file_id.
        """
        file = await self.get_file_cached(file_id)
        response = await self.__session.get(self.__file_url + file.file_path)
        return await response.read()


class ClassInit(type):

    def __init__(cls, *args):
        super().__init__(*args)
        cls.__classinit__()

    def __classinit__(self):
        pass


class BlockingTelegramAPI(Submethods, metaclass=ClassInit):

    @classmethod
    def __classinit__(cls):
        method_type = type(cls.__init__)
        for n in dir(TelegramAPI):
            func = getattr(TelegramAPI, n)
            if n.startswith('_') or type(func) != method_type:
                continue

            def blocking(f):
                return lambda self, *args, **kwargs: \
                    run_coroutine_threadsafe(f(self.__api, *args, **kwargs), self.__loop).result()

            setattr(cls, n, blocking(func))

    # we override all methods to call the actual API, no need to run superconstructor
    # noinspection PyMissingConstructor
    def __init__(self, api, loop):
        self.__api = api
        self.__loop = loop


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

    def with_root(self, path):
        self.__path = '.' + path
        return self

    def items(self):
        peer = self.__peer
        if not isinstance(peer, dict):
            raise DynamicTypeError(f'expected an object at {self.__path[1:]}, but it was '
                                   f'\'{type(peer).__name__}\'')
        return map(lambda k: (k, self[k]), peer)

    def get(self, item, default=None):
        try:
            return self[item]
        except NoSuchElementError:
            return default

    def __getattr__(self, item):
        peer = self.__peer
        if not isinstance(peer, dict):
            raise DynamicTypeError(f'expected an object at \'{self.__path[1:]}\', but it was '
                                   f'\'{type(peer).__name__}\'')
        path = f'{self.__path}.{item}'
        try:
            child = peer[item]
            # callables without arguments treated as properties
            # and callables with arguments are prohibited
            while callable(child):
                child = child()
        except (TypeError, KeyError):
            raise NoSuchElementError(path[1:]) from None
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
            raise DynamicTypeError(f'tried to index \'{type(peer).__name__}\' at {self.__path[1:]} with key of '
                                   f'type \'{type(item).__name__}\'') from None
        except (KeyError, IndexError):
            raise NoSuchElementError(path[1:]) from None
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


class IncorrectHandlerError(Exception):
    pass


class RequestError(IncorrectHandlerError):
    pass


class NoSuchElementError(IncorrectHandlerError):
    pass


class DynamicTypeError(IncorrectHandlerError):
    pass
