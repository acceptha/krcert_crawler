from slack_sdk import WebClient

from alarm.config import KrCertBot
from alarm.sender import SenderBase


class SlackSender(SenderBase):
    def __init__(self):
        self.client = WebClient(KrCertBot.BOT_TOKEN)
        self.channel = KrCertBot.MAIN_CHANNEL
        self.bot = "U07BKQ7BDB5"

    def get_last_notice(self):
        try:
            history = self.client.conversations_history(channel=self.channel, limit=10)
            for msg in history.data["messages"]:
                if msg["user"] == self.bot:
                    return msg["text"]
            raise Exception("Nothing message")
        except Exception as e:
            print(e)
            return ""

    def send_notice(self, krcert_info):
        try:
            sequence = [
                "title",
                "content",
                "link",
                "date",
            ]
            message = ""
            for key in filter(lambda x: krcert_info.get(x), sequence):
                if key == "title":
                    message += f"📢 *{krcert_info[key]}* 📢\n\n"
                elif key == "date":
                    message += f"<{krcert_info[key]}>"
                else:
                    message += f"{krcert_info[key]}\n\n"

            self.post_message(text=message)
        except Exception as e:
            print(e)

    def post_message(self, text):
        try:
            result = self.client.chat_postMessage(channel=self.channel, text=text)
            return result
        except Exception as e:
            print(e)

    def get_message_history(self, limit=100):
        try:
            history = self.client.conversations_history(channel=self.channel, limit=limit)
            return history.data["messages"]
        except Exception as e:
            print(e)

    def delete_message(self, timestamp):
        try:
            history = self.get_message_history()
            for msg in history:
                if msg["user"] == self.bot:
                    self.client.chat_delete(channel=self.channel, ts=timestamp)
        except Exception as e:
            print(e)
