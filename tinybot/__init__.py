
from traceback import print_exc
from inspect import signature

from tinybot.webapi import *
from tinybot.runner import *
import tinybot.logger as tlogger

__all__ = ('Bot', 'run')

logger = tlogger.get('tinybot')


class BotMeta(type):

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)
        cls.name = cls.name or cls.__name__
        cls.token = cls.token
        cls.version = cls.version
        cls.full_name = cls.name + '/' + cls.version
        cls.__callbacks = None
        cls.__instance = cls()

    def get_callbacks(cls):
        if not cls.__callbacks:
            callbacks = []
            for k in dir(cls):
                if k.startswith('handle_'):
                    callbacks.append(k[7:])
            cls.__callbacks = callbacks
        return cls.__callbacks

    def _process_update(cls, update, api):
        cls.__instance.update_id = update.update_id
        for name in update:
            if name == 'update_id':
                continue
            handler = getattr(cls.__instance, 'handle_' + name, None)
            if handler is None:
                logger.warning('received an update for \'%s\' update, but no handler exists for it', name)
                continue
            try:
                data = update[name]
                logger.debug('received \'%s\' update %s', name, data)
                try:
                    param_name = list(signature(handler).parameters)[0]
                except ValueError:
                    param_name = '<root>'
                DynamicDictObject.set_path(data, param_name)
                handler(data, api)
                logger.debug('handled \'%s\' update successfully', name)
            except RequestException as e:
                logger.warning('failed handling \'%s\' update, %s', name, e.args[0])
            except NoSuchElementException as e:
                logger.warning('failed handling \'%s\' update, no item \'%s\' found', name, e.args[0])
            except Exception:
                logger.error('unchecked exception while handling \'%s\' update:', name)
                print_exc()


    def update_webhook(cls, api, url):
        """Overridable if for whatever reason Telegram API for webhooks changes"""
        url = url + '/' + cls.token
        logger.info('getting webhook info')
        info = api.getWebhookInfo()
        callbacks = cls.get_callbacks()
        if info.url != url or set(info.allowed_updates) != set(callbacks):
            logger.info('setting webhook url to %s, and allowed updates to %s', url, callbacks)
            api.setWebhook(url=url, allowed_updates=callbacks)
        else:
            logger.info('webhook is correct')

    def launch_longpoll(cls, timeout):
        """Starts the longpoll loop with given timeout"""
        logger.info('starting longpoll loop with %s second timeout', timeout)
        with TelegramAPI(cls.name, cls.token) as api:
            try:
                callbacks = cls.get_callbacks()
                last = -1
                while True:
                    for update in api.getUpdates(offset=last + 1, allowed_updates=callbacks, timeout=timeout):
                        cls._process_update(update, api)
                        last = update.update_id
            except KeyboardInterrupt:
                logger.info('stopped longpoll loop due to interrupt signal')

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

        with TelegramAPI(cls.name, cls.token) as api:
            if url is not None:
                cls.update_webhook(api, url)

            server_logger = tlogger.get('tinybot.webhook')

            class PostRequestHandler(BaseHTTPRequestHandler):
                server_version = cls.full_name

                def do_POST(self):
                    self.send_response(HTTPStatus.OK)
                    self.end_headers()

                    if self.path[1:] != cls.token:
                        logger.warning('received POST request most likely not from Telegram servers')
                        return

                    post_data = self.rfile.read(int(self.headers.get('Content-Length', 0)))
                    data = json.loads(str(post_data, encoding='utf-8'))
                    cls._process_update(DynamicDictObject(data), api)

                def log_message(self, fmt, *args):
                    server_logger.debug(fmt, *args)

            logger.info('starting webhook server at port %s' % local_port)
            server = HTTPServer(('', local_port), PostRequestHandler)
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                logger.info('stopped webhook server due to interrupt signal')


class Bot(metaclass=BotMeta):
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

    def __init__(self):
        self.update_id = None
