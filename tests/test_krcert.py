import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd

from reference.krcert import get_table_info


def test_get_recent_krcert_info():
    info = dict(
        title='',
        date='',
        link='',
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
            break
    print(info)


def test_get_link_page_content():
    result = []
    table = {}
    table_index = 0

    # url = 'https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71543'
    # url = 'https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71540'
    url = 'https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71546'

    content_list = pd.read_html(url, encoding='utf-8')
    try:
        content = content_list[0].loc[0, 'Unnamed: 0']
    except Exception:
        content = content_list[0].loc[0, 0]
    content = content.replace(' ', ' ')

    if re.search('작성 ?: +위협 ?분석단 +취약점? ?분석팀', content, re.M):
        # 테이블 내 테이블 처리
        for idx, dataframe in enumerate(content_list[1:]):
            table[idx] = get_table_info(dataframe)

        # 내용 처리
        content = re.sub(r'\[\d+\]', '', content)
        for block in re.finditer('□([^□]+)', content, re.M):
            block = block.group(1)
            for i, line in enumerate(map(lambda x: x.strip(), block.split(' o '))):
                if i == 0:
                    name = line.strip()
                    if name in ('개요', '설명'):
                        result.append(f":white_medium_square: {name}")
                    else:
                        break
                else:
                    result.append(f"       {line}")

        print('\n'.join(result).strip())


def test_is_table():
    url = 'https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71555'
    # url = 'https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71540'

    response = urlopen(url=url)
    html = BeautifulSoup(markup=response, features='html.parser')
    html_parser = html.find('div', {'class': 'content_html'})
    table = html_parser.select('table')
    if table:
        value = True
    else:
        value = False

    print(value)


def test_get_table_info():
    dataframe = pd.DataFrame({
        0: ['취약점', 'CVE-2024-40766', 'CVE-2024-40766', 'CVE-2024-40766'],
        1: ['제품명', 'SOHO (Gen5)', 'Gen6 방화벽 - SOHOW, TZ 300, TZ 300W, TZ 400, TZ 400W, TZ 500, TZ 500W, TZ 600, NSA 2650,\xa0NSA 3600, NSA 3650, NSA 4600, NSA 4650, NSA 5600, NSA 5650, NSA 6600, NSA 6650, SM 9200, SM 9250, SM 9400, SM 9450, SM 9600, SM 9650, TZ 300P, TZ 600P, SOHO 250, SOHO 250W, TZ 350, TZ 350W', 'Gen7 방화벽 - TZ270, TZ270W, TZ370, TZ370W, TZ470, TZ470W, TZ570, TZ570W, TZ570P, TZ670, NSa 2700, NSa 3700, NSa 4700, NSa 5700, NSa 6700, NSsp 10700, NSsp 11700, NSsp 13700'],
        2: ['영향받는 버전', '5.9.2.14-12o 이하', '6.5.4.14-109n 이하', 'SonicOS 빌드 버전 7.0.1-5035'],
        3: ['해결 버전', '5.9.2.14-13o', '6.5.2.8-2n (SM9800, NSsp 12400, NSsp 12800용), 6.5.4.15.116n(다른 Gen6 방화벽 어플라이언스용)', 'SonicOS 빌드 버전 7.0.1-5035 이후'],
    })
    table_info = dict(column=[])

    for i, row in dataframe.iterrows():
        if i == 0:
            table_info['column'] = list(row.values)
        else:
            table_info.setdefault(i - 1, list())
            table_info[i - 1] = list(row.values)

    print(table_info)


def test_get_html_of_link_page():
    # url = 'https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71543'
    url = 'https://www.krcert.or.kr/kr/bbs/view.do?searchCnd=&bbsId=B0000133&searchWrd=&menuNo=205020&pageIndex=1&categoryCode=&nttId=71540'

    response = urlopen(url=url)
    html = BeautifulSoup(markup=response, features='html.parser')
    html_parser = html.find('div', {'class': 'content_html'})
    rs = str(html_parser)
    print(rs)
