import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import make_msgid
from reference.krcert import get_html_of_link_page


def test_get_last_notice():
    pass


def test_send_notice():
    from_email = 'admin@ssrinc.co.kr'
    to_emails = ['siha@ssrinc.co.kr']

    # url = 'https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71543'
    url = 'https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71540'
    content = get_html_of_link_page(url)

    # SMTP 서버 정보
    smtp_server = "192.168.1.200"
    smtp_port = 25
    smtp_timeout = 1000

    for to_email in to_emails:
        # 이메일 메시지 구성
        message = MIMEMultipart()
        message["From"] = from_email
        message["To"] = to_email
        message["Subject"] = "📢 보안 공지"
        message['Message-id'] = make_msgid()

        # 이메일 본문 추가
        # message.attach(MIMEText(body, "plain", "utf8"))
        message.attach(MIMEText(content, "html", "utf8"))
        # message.attach(
        #     MIMEText(
        #         '<html><head><style>a {text-decoration: none;} a:hover {text-decoration: underline;}</style></head><body style="margin-left: 40px;">' +
        #         body +
        #         '</body></html>',
        #         'html',
        #         'utf-8'
        #     )
        # )

        # s = smtplib.SMTP(smtp_server, smtp_port, timeout=timeout)
        # s = smtplib.SMTP_SSL(host=smtp_server, port=smtp_port, timeout=timeout)
        # s = smtplib.LMTP(host=smtp_server, port=smtp_port, timeout=timeout)

        # SSL을 사용하여 SMTP 서버와 연결
        # context = ssl.create_default_context()
        # with smtplib.SMTP_SSL("192.168.1.200", 465, context=context) as server:
        # with smtplib.SMTP_SSL("192.168.1.200", 25) as server:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=smtp_timeout) as server:
            try:
                server.ehlo()
                # if rs[0] == 250:
                #     server.starttls()
                #     server.ehlo()
                #     로그인
                #     server.login(user='root', password='qwe')
                # 이메일 전송
                server.sendmail('admin@ssrinc.co.kr', 'siha@ssrinc.co.kr', message.as_string())
            except smtplib.SMTPNotSupportedError as smtp_not_auth_e:
                # 메일 서버에서 TLS 인증을 지원하지 않는 경우 로그인이 필요없음
                print(smtp_not_auth_e)
            except smtplib.SMTPAuthenticationError as smtp_auth_e:
                print(smtp_auth_e)  # 아이디/패스워드 오류
            except smtplib.SMTPException as smtp_e:
                print(smtp_e)  # 메일 서버 연결 실패
            except Exception as e:
                print(f"이메일 전송 중 오류가 발생했습니다: {e}")

        print("이메일이 성공적으로 전송되었습니다.")
