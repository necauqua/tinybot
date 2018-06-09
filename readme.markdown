# tinybot
This is a small and simple library for quickly building Telegram Bots with Python.

It is made to be dynamic and independent of the Telegram Bot API.
It means that whenever a new Telegram API method or callback is added,
there is no need to update this library, all calls are dynamic and you can send whatever you like to Telegram.

## Installation
It is published on PyPI so to use it simply install it with pip.
```
$ pip install tinybot
```

## Example
Actually working little bot (from which this library was originated) can be found [here](https://github.com/necauqua/county-bot).

Here is a simple example:
```python

import tinybot


class Assistant(tinybot.Bot):
    version = '0.0.1-SNAPSHOT'
    token = '123456789:token-for-debugging' # token is not required when using tinybot.run

    def handle_message(self, data, api):
        if '@all' in data.text:
            api.sendMessage(chat_id=data.chat.id, text='@necauqua @other_people..')
            api.sendMessage(chat_id=data.chat.id, text='[debug] update id ' + str(self.update_id))


if __name__ == '__main__':
    # just start longpoll loop for debugging
    Assistant.launch_longpoll(30)

    # tinybot.run is a ready-to-use CLI for launching longpoll or webhook and providing the token
    # tinybot.run(Assistant, 'necauqua assistant bot')

```

## Usage
Your bot is a class which derives from `tinybot.Bot` class.
You can start it with a ready-to-use CLI using this standard construct
```python
if __name__ == '__main__':
    tinybot.run(bot_cls, bot_description)
```
All of the bot's logic is defined inside the class deriven from `tinybot.Bot`.

It have static fields `name`, `version`,`full_name` and `token`.
* `name` defaults to the class name and is the name of your bot. Used in `full_name`
* `version` is a version of your bot, it defaults to `0.1.0`. Used in `full_name`.
* `full_name` defaults to `name/version`.
It is used as a `User-Session` header when making requests, and as `Server` header when
responding to Telegram from a webhook server.
* `token` is an optional field, because usually it is set from command line when running `tinybot.run`.
However, it might be useful for debugging.
It is obviously the token which is used for all requests.

Your class should define methods with signarure `handle_xxx(self, data, api)` where `xxx` is one of the update types found [here](https://core.telegram.org/bots/api#getting-updates).

For example:
```python
def handle_message(self, message, api): pass
# or
def handle_channel_post(self, post, api): pass
```
* `self` parameter can contain some additional data, for now it only contains the `update_id` field.
* `data` parameter is a dict/list-like recursive structure made with `__getattr__`'s
and `__getitems__`'s in which the received Update JSON object is given.
When you try to get a nonexistent field, `NoSuchElementException` is raised and
then handled properly by the `launch_xxx` methods caller.
* `api` parameter worls similarly, any method call which looks like
`api.anyMethodCall(**kwargs)` would send appropriate request to the Telegram Bot API.<br>
When you do such a request, Telegram returns JSON in format <br>
`{"ok": true, "update": ..data..}`<br>or<br>
`{"ok": false, "description": "..error message.."}`.<br>
This JSON is unwrapped and if ok is false or non-existent, `RequestException` is raised
with the description and similarly handled by the `launch_xxx` methods caller.
Else, the `"update"` object is wrapped in the same structure as the `data` parameter and
is returned from the `api` method call.

All of the above means that if you want your bot to do multiple get-and-then-send requests,
you'll want to arrange your code to first get all the data and only after that send your requests.
That way, if any of the data weren't available, any of your mutating requests would not be sent.

## License
It is licensed under permissive MIT license which means you can use this code in
whatever way possible, as long as you include the LICENSE file (by which you mention my authorship).
It is included in the package so you have to do nothing yourself when simply using this library.