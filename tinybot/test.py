import asyncio

import tinybot


@tinybot.debug_run(tokenfile='/etc/tg-notification-bot-token')
class TestBot(tinybot.Bot):

    def handle_message(self, data, api):
        if 'test' in data.text:
            api.sendMessage(chat_id=data.chat.id, text='hello world')
        # if 'document' in data:
        #     print(str(api.download(data.document.file_id), 'utf-8'))

