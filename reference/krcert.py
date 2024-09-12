import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


def get_recent_krcert_info():
    info = dict(
        title='',
        date='',
        link='',
        content='',
    )

    # 보안 공지 홈페이지 확인
    url = 'https://www.krcert.or.kr/kr/bbs/list.do?menuNo=205020&bbsId=B0000133'
    response = urlopen(url=url)
    html = BeautifulSoup(markup=response, features='html.parser')

    table_list = html.select('table > tbody > tr')
    for row in table_list:
        title = row.find('td', {'class': 'sbj tal'})
        date = row.find('td', {'class': 'date'})
        link_tag = row.select_one('a')
        if title and date and link_tag:
            info['title'] = title.text.strip()
            info['date'] = date.text.strip()
            info['link'] = f"https://www.krcert.or.kr{link_tag.get('href')}"
            info['content'] = get_link_page_content(info['link'])
            return info


def get_link_page_content(url) -> str:
    result = []
    table = {}

    content_list = pd.read_html(url, encoding='utf-8')
    content = content_list[0][0][0]

    if re.search('□ +작성 ?: +위협 ?분석단 +취약점? ?분석팀', content, re.M):
        # 테이블 내 테이블 처리
        for table_index, table_pandas in enumerate(content_list[1:]):
            table_key = ''
            for i, row in content_list[table_index + 1].iterrows():
                if i == 0:
                    table_key = row.values[0].split()[0]
                    table.setdefault(table_key, [])
                    table[table_key].append('\t'.join(row.values))
                    table[table_key].append('-' * 80)
                else:
                    table[table_key].append('\t'.join(row.values))

        # 내용 처리
        content = re.sub(r'\[\d+\]', '', content)
        for block in re.finditer('□([^□]+)', content, re.M):
            block = block.group(1)
            table_key = ''
            for i, line in enumerate(map(lambda x: x.strip(), block.split(' o '))):
                if i == 0:
                    tmp = line.split()
                    name = line
                    if len(tmp) > 1:
                        for key in table.keys():
                            if key in tmp:
                                table_key = key
                                idx = tmp.index(key)
                                name = ' '.join(tmp[:idx])
                    if name in ('문의사항') or tmp[0] in ('참고사이트', '작성:'):
                        break
                    result.append(f":white_medium_square: {name}")
                else:
                    result.append(f"       {line}")

                if table_key:
                    result.extend(table[table_key])

    return '\n'.join(result)


def get_html_of_link_page(url):
    response = urlopen(url=url)
    html = BeautifulSoup(markup=response, features='html.parser')
    html_parser = html.find('div', {'class': 'content_html'})
    return str(html_parser)
