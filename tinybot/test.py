import io

import tinybot


class TestBot(tinybot.Bot):

    async def handle_message(self, data, _):
        print(data)
        pass


if __name__ == '__main__':

    import tinybot.typez

    print(tinybot.typez.User(123, True, 'testbot'))
    print(tinybot.typez.WebhookInfo('url', False, 0, max_connections=123))

    exit(0)
    with open('/etc/tg-notification-bot-token', 'r') as f:
        line = f.readline().strip()
        TestBot.token = line[line.find('=') + 1:]

        async def action(api: tinybot.TelegramAPI):

            # await api.send_document(chat_id='590866023', document=('test.txt', io.StringIO('some test file')))
            await api.send_document(chat_id='325827733', document=('test.txt', io.StringIO('some test file')))

        TestBot.run_blocking(action)
