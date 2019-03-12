
import tinybot


class TestBot(tinybot.Bot):

    def handle_message(self, data, api):
        if 'hui' in data.text:
            api.sendMediaGroup(chat_id=data.chat.id, media=[{'type': 'photo', 'media': 'attach://test'}], test=open('/home/abulakh/Documents/avatar.jpeg', 'rb'))


if __name__ == '__main__':
    with open('/etc/tg-notification-bot-token') as f:
        TestBot.token = f.read()[13:-1]
    TestBot.launch_longpoll(30)
