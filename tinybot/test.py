import io

import tinybot


class TestBot(tinybot.Bot):

    async def handle_message(self, data, _):
        print(data)
        pass


if __name__ == '__main__':
    with open('/etc/tg-notification-bot-token', 'r') as f:
        line = f.readline().strip()
        TestBot.token = line[line.find('=') + 1:]

        async def action(api):
            # await api.sendDocument(chat_id='590866023', document=('test.txt', io.StringIO('some test file')))
            await api.sendDocument(chat_id='325827733', document=('test.txt', io.StringIO('some test file')))

        TestBot.run_blocking(action)
