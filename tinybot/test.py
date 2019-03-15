import asyncio, aiohttp

import tinybot


@tinybot.debug_run(tokenfile='/etc/tg-notification-bot-token')
class TestBot(tinybot.Bot):

    async def handle_message(self, data, api):
        if 'test' in data.text:
            # await api.sendPhoto(chat_id=data.chat.id, photo=open('/home/abulakh/Pictures/test.png', 'rb'))
            import io
            await api.sendDocument(chat_id=data.chat.id, document=('test.txt', io.StringIO('kek lol cheburek\n')))
        # if 'document' in data:
        #     print(str(api.download(data.document.file_id), 'utf-8'))


# async def main():
#     async with aiohttp.ClientSession() as session:
#         api = tinybot.TelegramAPI(session, '')
#         api._TelegramAPI__url = 'http://localhost:8080/'
#         import io
#         await api.sendDocument(chat_id=123, document=('test.txt', io.StringIO('kek lol cheburek\n')))
#
#         pass
#
# if __name__ == '__main__':
#     asyncio.get_event_loop().run_until_complete(main())
