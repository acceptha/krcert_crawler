import re

from alarm.slack import SlackMessenger
from reference.krcert import get_recent_krcert_info


def send_notification_to_slack():
    pre_date = ''

    sm = SlackMessenger()
    last_notice = sm.get_last_notice()
    regex = re.search(r'&lt;(?P<date>\d+-\d+-\d+)&gt;$', last_notice, re.M)
    if regex:
        pre_date = regex.group('date')

    is_update = False
    post_info = get_recent_krcert_info()
    if pre_date == post_info['date']:
        is_update = True

    if not is_update:
        sequence = ['title', 'link', 'date', 'content']
        message = ''
        for key in sequence:
            if key == 'title':
                message += f"📢: {post_info[key]}\n"
            elif key == 'date':
                message += f"<{post_info[key]}>"
            else:
                message += f"{post_info[key]}\n"

        sm.post_notice(message)


if __name__ == '__main__':
    send_notification_to_slack()
