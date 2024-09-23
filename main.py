import re

from alarm.slack_service import SlackSender
from reference.krcert import iter_recent_krcert_info


def send_notification_to_slack():
    posting_info = []

    sm = SlackSender()
    last_notice = sm.get_last_notice()

    link_id_pattern = re.compile(r'nttid=(\d+)', re.M | re.I)
    regex = link_id_pattern.search(last_notice)
    if regex:
        pre_link_id = regex.group(1)
    else:
        pre_link_id = 0

    for krcert_info in iter_recent_krcert_info():
        regex = link_id_pattern.search(krcert_info['link'])
        post_link_id = regex.group(1)
        if pre_link_id and pre_link_id == post_link_id:
            break
        elif not pre_link_id and posting_info:
            # break
            posting_info.append(krcert_info.copy())
        else:
            posting_info.append(krcert_info.copy())

    for info in reversed(posting_info):
        sm.send_notice(info)


if __name__ == '__main__':
    send_notification_to_slack()
