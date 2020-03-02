from typing import *

Response = Union[Awaitable[...], ...]

class Message:
    """This is a stub message todo lol"""


class TelegramAPI:

    def __init__(self, session, token) -> None: ...

    def safe(self, retries) -> TelegramAPI: ...

    def sendDocument(self, *, chat_id: Union[str, int], **kwargs) -> Response:
        """
        Use this method to send general files. On success, the sent :class:`Message` is returned. Bots can currently send files of any type of up to 50 MB in size, this limit may be changed in the future.

        :param chat_id Unique identifier for the target chat or username of the target channel (in the format `@channelusername`)
        """
        ...


