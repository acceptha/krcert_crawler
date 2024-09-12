from slack_sdk import WebClient

from alarm.config import KrCertBot


def test_get_last_notice():
    bot = 'U07BKQ7BDB5'
    client = WebClient(KrCertBot.BOT_TOKEN)
    channel = KrCertBot.TEST_CHANNEL

    try:
        history = client.conversations_history(channel=channel, limit=50)
        for msg in history.data['messages']:
            if msg['user'] == bot and msg['text'].startswith(r'📢 보안공지\n'):
                return True, msg['text']
        print(False, '')
    except Exception as e:
        print(e)


def test_send_notice():
    client = WebClient(KrCertBot.BOT_TOKEN)
    channel = KrCertBot.TEST_CHANNEL
    text = """
    """

    try:
        text = r'📢 보안공지\n' + text
        result = client.chat_postMessage(channel=channel, text=text)
        return result
    except Exception as e:
        print(e)


def test_get_message_history():
    client = WebClient(KrCertBot.BOT_TOKEN)
    channel = KrCertBot.TEST_CHANNEL
    limit = 100

    try:
        history = client.conversations_history(channel=channel, limit=limit)
        return history.data['messages']
    except Exception as e:
        print(e)


def test_delete_message():
    client = WebClient(KrCertBot.BOT_TOKEN)
    channel = KrCertBot.MAIN_CHANNEL
    limit = 100
    bot = 'U07BKQ7BDB5'

    try:
        history = client.conversations_history(channel=channel, limit=limit)
        for msg in history.data['messages']:
            if msg['user'] == bot:
                client.chat_delete(channel=channel, ts=msg['ts'])
    except Exception as e:
        print(e)
