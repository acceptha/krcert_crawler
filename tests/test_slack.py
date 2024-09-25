from slack_sdk import WebClient

from alarm.config import KrCertBot


def test_get_last_notice():
    bot = "U07BKQ7BDB5"
    client = WebClient(KrCertBot.BOT_TOKEN)
    channel = KrCertBot.TEST_CHANNEL

    try:
        history = client.conversations_history(channel=channel, limit=50)
        for msg in history.data["messages"]:
            if msg["user"] == bot and msg["text"].startswith(r"📢 보안공지\n"):
                return True, msg["text"]
        print(False, "")
    except Exception as e:
        print(e)


def test_send_notice():
    client = WebClient(KrCertBot.BOT_TOKEN)
    channel = KrCertBot.TEST_CHANNEL
    krcert_info = {
        "title": "SonicWall 제품 보안 업데이트 권고",
        "date": "2024-09-12",
        "link": "https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71546",
        "content": ":white_medium_square: 개요\n       SonicWall社는 자사 제품에서 발생하는 취약점을 해결한 업데이트 버전 배포\n       영향받는 버전을 사용 중인 시스템 사용자는 해결 방안에 따라 최신 버전으로 업데이트 권고\n:white_medium_square: 설명\n       SonicWall의 SonicOS에서 발생하는 부적절한 접근 제어 취약점(CVE-2024-40766)",
    }

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

        result = client.chat_postMessage(channel=channel, text=message)
    except Exception as e:
        print(e)


def test_post_message():
    client = WebClient(KrCertBot.BOT_TOKEN)
    channel = KrCertBot.TEST_CHANNEL
    text = "test"

    try:
        result = client.chat_postMessage(channel=channel, text=text)
        print(result)
    except Exception as e:
        print(e)


def test_get_message_history():
    client = WebClient(KrCertBot.BOT_TOKEN)
    channel = KrCertBot.TEST_CHANNEL
    limit = 100

    try:
        history = client.conversations_history(channel=channel, limit=limit)
        return history.data["messages"]
    except Exception as e:
        print(e)


def test_delete_message():
    client = WebClient(KrCertBot.BOT_TOKEN)
    channel = KrCertBot.MAIN_CHANNEL
    limit = 100
    bot = "U07BKQ7BDB5"

    try:
        history = client.conversations_history(channel=channel, limit=limit)
        for msg in history.data["messages"]:
            if msg["user"] == bot:
                client.chat_delete(channel=channel, ts=msg["ts"])
    except Exception as e:
        print(e)
