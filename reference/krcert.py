import re
from urllib.request import urlopen

import pandas as pd
from bs4 import BeautifulSoup


def iter_recent_krcert_info_using(content):
    if content not in ("text", "html"):
        raise Exception

    info = dict(
        title="",
        date="",
        link="",
        content="",
    )

    # 보안 공지 홈페이지 확인
    url = "https://www.krcert.or.kr/kr/bbs/list.do?menuNo=205020&bbsId=B0000133"
    response = urlopen(url=url)
    html = BeautifulSoup(markup=response, features="html.parser")

    table_list = html.select("table > tbody > tr")
    for row in table_list:
        title = row.find("td", {"class": "sbj tal"})
        date = row.find("td", {"class": "date"})
        link_tag = row.select_one("a")
        if title and date and link_tag:
            info["title"] = title.text.strip()
            info["date"] = date.text.strip()
            info["link"] = f"https://www.krcert.or.kr{link_tag.get('href')}"
            if content == "text":
                info["content"] = get_link_page_plain(info["link"])
            else:
                info["content"] = get_link_page_html(info["link"])
            yield info


def get_link_page_plain(url) -> str:
    result = []
    table = {}

    if is_table(url):
        content_list = pd.read_html(url, encoding="utf-8")
        try:
            content = content_list[0].loc[0, "Unnamed: 0"]
        except Exception:
            content = content_list[0].loc[0, 0]
        content = content.replace(" ", " ")

        if re.search("작성 ?: +위협 ?분석단 +취약점? ?분석팀", content, re.M):
            # 테이블 내 테이블 처리
            for table_index, table_pandas in enumerate(content_list[1:]):
                table[table_index] = get_table_info(table_pandas)

            # 내용 처리
            content = re.sub(r"\[\d+\]", "", content)
            for block in re.finditer("□([^□]+)", content, re.M):
                block = block.group(1)
                for i, line in enumerate(map(lambda x: x.strip(), block.split(" o "))):
                    if i == 0:
                        name = line.strip()
                        if name in ("개요", "설명"):
                            result.append(f":white_medium_square: {name}")
                        else:
                            break
                    else:
                        result.append(f"       {line}")

    return "\n".join(result).strip()


def is_table(url):
    response = urlopen(url=url)
    html = BeautifulSoup(markup=response, features="html.parser")
    html_parser = html.find("div", {"class": "content_html"})
    table = html_parser.select("table")
    if table:
        return True
    else:
        return False


def get_table_info(dataframe):
    table_info = dict(column=[])

    for i, row in dataframe.iterrows():
        if i == 0:
            table_info["column"] = list(row.values)
        else:
            table_info.setdefault(i - 1, list())
            table_info[i - 1] = list(row.values)

    return table_info


def get_link_page_html(url):
    response = urlopen(url=url)
    html = BeautifulSoup(markup=response, features="html.parser")
    html_parser = html.find("div", {"class": "content_html"})
    html_content = str(html_parser)
    for link in re.finditer(r"<img [^>]+src=\"(?P<src>[^\"]+)\" [^>]+>", html_content, re.I | re.M):
        html_content = html_content.replace(link.group("src"), f"https://www.krcert.or.kr{link.group('src')}")
    return html_content
