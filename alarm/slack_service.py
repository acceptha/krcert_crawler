from slack_sdk import WebClient

from alarm.sender import SenderBase
from alarm.config import KrCertBot


class SlackSender(SenderBase):
    def __init__(self):
        self.client = WebClient(KrCertBot.BOT_TOKEN)
        self.channel = KrCertBot.MAIN_CHANNEL
        self.bot = 'U07BKQ7BDB5'

    def get_last_notice(self):
        try:
            history = self.client.conversations_history(channel=self.channel, limit=10)
            for msg in history.data['messages']:
                if msg['user'] == self.bot:
                    return msg['text']
            raise Exception("Nothing message")
        except Exception as e:
            print(e)
            return ''

    def send_notice(self, content):
        try:
            result = self.client.chat_postMessage(channel=self.channel, text=content)
            return result
        except Exception as e:
            print(e)

    def get_message_history(self, limit=100):
        try:
            history = self.client.conversations_history(channel=self.channel, limit=limit)
            return history.data['messages']
        except Exception as e:
            print(e)

    def delete_message(self, timestamp):
        try:
            history = self.get_message_history()
            for msg in history:
                if msg['user'] == self.bot:
                    self.client.chat_delete(channel=self.channel, ts=timestamp)
        except Exception as e:
            print(e)
