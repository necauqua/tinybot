from asyncio import iscoroutinefunction
from inspect import signature
from traceback import print_exc

from aiohttp import ClientSession

import tinybot.logger as tlogger
from tinybot.runner import *
from tinybot.webapi import *

__all__ = ('Bot', 'run', 'debug_run')

logger = tlogger.get('tinybot')


def setup_handlers(cls, api):
    instance = cls()
    handlers = {}
    for k in dir(cls):
        if not k.startswith('handle_'):
            continue
        name = k[7:]
        func = getattr(instance, 'handle_' + name, None)
        if func is None:
            logger.warning('received an update for \'%s\' update, but no handler exists for it', name)
            continue

        if not iscoroutinefunction(func):
            loop = asyncio.get_event_loop()
            blocking_api = BlockingTelegramAPI(api, loop)

            async def handler(d):
                return await loop.run_in_executor(None, lambda: func(d, blocking_api))
        else:
            def handler(d):
                return func(d, api)

        handlers[name] = handler
    return handlers


async def receive_update(handlers, update):
    for name in update:
        if name == 'update_id':
            continue

        handler = handlers.get(name)
        if not handler:
            logger.warning('received an update for \'%s\' update, but no handler exists for it', name)

        # noinspection PyBroadException
        try:
            data = update[name]
            logger.debug('received \'%s\' update %s', name, data)
            try:
                param_name = list(signature(handler).parameters)[0]
            except ValueError:
                param_name = '<root>'

            DynamicDictObject.set_path(data, param_name)

            await handler(data)

            logger.debug('handled \'%s\' update successfully', name)
        except RequestException as e:
            logger.warning('failed handling \'%s\' update, %s', name, e.args[0])
        except NoSuchElementException as e:
            logger.warning('failed handling \'%s\' update, no item \'%s\' found', name, e.args[0])
        except Exception:
            logger.error('unchecked exception while handling \'%s\' update:', name)
            print_exc()


def create_session(cls):
    return ClientSession(headers={'User-Agent': cls.full_name, 'Accept': 'application/json'})


class Bot:
    """
    Extend this class to define a Telegram Bot.
    Methods with signature `handle_xxx(self, data, api)` will be called
    for `xxx` update events from Telegram Bot API when the bot is started
    either with `launch_longpoll` or `launch_webhook`.

    The `data` parameter is a dict/list-like recursive structure made with __getattr__'s
    and __getitems__'s in which the received Update JSON object is given.
    When you try to get a nonexistent field, `NoSuchElementException` is raised and
    then handled properly by the `launch_xxx` methods.

    The `api` parameter worls similarly, any method call which looks like
    `api.anyMethodCall(**kwargs)` would send a request to the Telegram Bot API.

    When you do such a request, Telegram returns JSON in format
    `{"ok": true, "update": ..data..}` or
    `{"ok": false, "description": "..error message.."}`.
    This JSON is unwrapped and if ok is false or non-existent, `RequestException` is raised
    and similarly handled by the `launch_xxx` methods.
    Else, the `"update"` object is wrapped in the same structure as the `data` parameter and
    is returned from the api method call.
    """

    name = None
    """Name of the bot, defaults to class name"""

    full_name = None
    """Full name of the bot, defaults to 'name/version'"""

    description = 'Telegram Bot'
    """Optional extended description of the bot, right now it is only used in CLI help"""

    version = '0.1.0'
    """Version of the bot"""

    token = None
    """Token to be used by this bot, usually not set directly in class definition"""

    def __init_subclass__(cls, **kwargs):
        cls.name = cls.name or cls.__name__
        cls.full_name = cls.name + '/' + cls.version

    @classmethod
    async def update_webhook(cls, api, url, allowed_updates, max_connections=40):
        """Overridable if for whatever reason Telegram API for webhooks changes"""
        url = url + '/' + cls.token
        logger.info('getting webhook info')
        info = await api.getWebhookInfo()
        if info.url != url \
                or set(info.allowed_updates) != set(allowed_updates) \
                or info.get('max_connections') != max_connections:
            logger.info('setting webhook url to %s, and allowed updates to %s', url, allowed_updates)
            await api.setWebhook(url=url, allowed_updates=allowed_updates, max_connections=max_connections)
        else:
            logger.info('webhook is correct')

    @classmethod
    def launch_longpoll(cls, timeout):
        """Starts the longpoll loop with given timeout"""
        logger.info('starting longpoll loop with %s second timeout', timeout)

        async def go():
            async with create_session(cls) as session:
                api = TelegramAPI(session, cls.token)
                handlers = setup_handlers(cls, api)
                callbacks = list(handlers.keys())
                last_id = -1
                tasks = []

                while True:
                    for update in await api.getUpdates(offset=last_id + 1, allowed_updates=callbacks, timeout=timeout):
                        tasks.append(asyncio.ensure_future(receive_update(handlers, update)))
                        last_id = update.update_id

                    while len(tasks) > 100:
                        await tasks[0]

        try:
            asyncio.get_event_loop().run_until_complete(go())
        except KeyboardInterrupt:
            logger.info('stopped longpoll loop due to interrupt signal')

    @classmethod
    def launch_webhook(cls, url, local_port=None):
        """
        Starts the webhook server (automatically setting the webhook data) with given host and port.
        Note that host is used to set the webhook as well as to launch python's http server
        """

        # url is optional so shift args accordingly
        if local_port is None:
            local_port = url
            url = None

        import json
        from http import HTTPStatus
        from http.server import BaseHTTPRequestHandler, HTTPServer

        async def go():
            async with create_session(cls) as session:
                api = TelegramAPI(session, cls.token)
                handlers = setup_handlers(cls, api)

                if url is not None:
                    await cls.update_webhook(api, url, list(handlers.keys()))

                server_logger = tlogger.get('tinybot.webhook')

                class PostRequestHandler(BaseHTTPRequestHandler):
                    server_version = cls.full_name

                    def do_POST(self):
                        nonlocal cls

                        self.send_response(HTTPStatus.OK)
                        self.end_headers()

                        if self.path[1:] != cls.token:
                            logger.warning('received POST request most likely not from Telegram servers')
                            return

                        post_data = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                        data = json.loads(str(post_data, encoding='utf-8'))
                        receive_update(cls, DynamicDictObject(data))

                    def log_message(self, fmt, *args):
                        server_logger.debug(fmt, *args)

                logger.info('starting webhook server at port %s' % local_port)
                server = HTTPServer(('', local_port), PostRequestHandler)
                server.serve_forever()

        try:
            asyncio.get_event_loop().run_until_complete(go())
        except KeyboardInterrupt:
            logger.info('stopped webhook server due to interrupt signal')
