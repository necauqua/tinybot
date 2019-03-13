import tinybot


class TestBot(tinybot.Bot):

    def handle_message(self, data, api):
        if 'document' in data:
            print(str(api.download(data.document.file_id), 'utf-8'))


if __name__ == '__main__':
    with open('/etc/tg-notification-bot-token') as f:
        line = f.readline()[:-1]
        TestBot.token = line[line.index('=') + 1:] if '=' in line else line
    TestBot.launch_longpoll(30)
