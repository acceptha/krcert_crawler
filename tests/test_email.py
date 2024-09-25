import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid

from alarm.config import SMTP


def test_get_last_notice():
    pass


def test_send_notice():
    # SMTP 서버 정보
    local = "my"
    if local == "ssr":
        smtp_server = "192.168.1.200"
        smtp_port = 25
    else:
        smtp_server = "smtp.gmail.com"
        smtp_port = 587

    krcert_info = {
        "title": "SonicWall 제품 보안 업데이트 권고",
        "date": "2024-09-12",
        "link": "https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71546",
        "content": ":white_medium_square: 개요\n       SonicWall社는 자사 제품에서 발생하는 취약점을 해결한 업데이트 버전 배포\n       영향받는 버전을 사용 중인 시스템 사용자는 해결 방안에 따라 최신 버전으로 업데이트 권고\n:white_medium_square: 설명\n       SonicWall의 SonicOS에서 발생하는 부적절한 접근 제어 취약점(CVE-2024-40766)",
    }

    # url = 'https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71543'
    # url = 'https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71540'
    url = "https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71555"

    # 이메일 메시지 구성
    message = MIMEMultipart()
    message["From"] = SMTP.FROM_EMAIL
    message["To"] = ", ".join(SMTP.TO_EMAIL)
    message["Subject"] = f"📢 {krcert_info['title']} 📢"
    message["Message-id"] = make_msgid()

    # 이메일 본문 추가
    # message.attach(MIMEText(content, "plain", "utf8"))  # MIMEMultipart
    message.attach(MIMEText(krcert_info["content"], "html", "utf8"))  # MIMEMultipart

    # SSL을 사용하여 SMTP 서버와 연결 후 이메일 전송
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.ehlo()
        server.starttls()
        server.login(user=SMTP.USER, password=SMTP.PASSWD)
        server.send_message(message)
        # server.sendmail(message["From"], message["To"], message.as_string())
    except smtplib.SMTPNotSupportedError as smtp_not_auth_e:
        # 메일 서버에서 TLS 인증을 지원하지 않는 경우 로그인이 필요없음
        print(smtp_not_auth_e)
    except smtplib.SMTPAuthenticationError as smtp_auth_e:
        print(smtp_auth_e)  # 아이디/패스워드 오류
    except smtplib.SMTPException as smtp_e:
        print(smtp_e)  # 메일 서버 연결 실패
    except Exception as e:
        print(f"이메일 전송 중 오류가 발생했습니다: {e}")
    # s = smtplib.LMTP(host=smtp_server, port=smtp_port, timeout=timeout)
    # with smtplib.SMTP_SSL("192.168.1.200", 465, context=context) as server:
    # with smtplib.SMTP_SSL("192.168.1.200", 25) as server:

    # if rs[0] == 250:
    #     server.starttls()
    #     server.ehlo()
    #     로그인
    #     server.login(user='root', password='qwe')
    # 이메일 전송

    print("이메일이 성공적으로 전송되었습니다.")
