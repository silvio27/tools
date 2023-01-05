#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Project  : Oxford_dictionary_word_search
# @Time     : 2023/1/5 9:41
# @Author   : Silvio
# @Email    : goblin-sun@hotmail.com


import requests
from bs4 import BeautifulSoup


def get_html(word='dick'):
    """
    获得 oxfordlearnersdictionaries 对单词的解释

    :param word: 查询的单词
    :return: 解释内容
    """
    # word = 'reluctant'
    # word = 'torpedo'
    # word = 'dick'
    url = f'https://www.oxfordlearnersdictionaries.com/definition/english/{word}/?q={word}'

    cookies = {
        'localisation': 'CN',
        'JSESSIONID': 'C28D204CC4B057B3AFFD9F5B175C3A9B',
        'dictionary': 'english',
        'iawpvccs': '1',
        'iawpvc': '1',
        '_ga': 'GA1.2.1165123822.1672882457',
        '_gid': 'GA1.2.1255372467.1672882457',
        '_pbjs_userid_consent_data': '3524755945110770',
        '_sharedID': 'ecaeec57-2e95-4b74-b8c8-41277df20e7f',
        'iawppid': 'a2b6f24d031948bbad1aff6c5b15afe9',
        '_hjSessionUser_951831': 'eyJpZCI6IjM5MGYyZGVkLTFmMDctNTAzMy1hZDAwLWUxZjEwZjQ3NDdhOCIsImNyZWF0ZWQiOjE2NzI4ODI0NTk2MzksImV4aXN0aW5nIjpmYWxzZX0=',
        '_hjFirstSeen': '1',
        '_hjSession_951831': 'eyJpZCI6IjE0NmM0ZmExLWViY2MtNDNkOS04MDMzLTJmMGY2ZmYyNWY0YyIsImNyZWF0ZWQiOjE2NzI4ODI0NjA0MjEsImluU2FtcGxlIjpmYWxzZX0=',
        '_hjAbsoluteSessionInProgress': '0',
        '__gads': 'ID=fe5d890bc51b0646:T=1672882460:S=ALNI_MbfG_gQzWo2uFiI6UjcKFIpAmjXTg',
        '__gpi': 'UID=00000b9e61bc553a:T=1672882460:RT=1672882460:S=ALNI_MbLg9SR6hlK9JVVPd1ISs__gDLHww',
        '_lr_retry_request': 'true',
        '_lr_env_src_ats': 'false',
        'pbjs-unifiedid': '%5Bobject%20Object%5D',
        'cto_bundle': 'R-Y8fV9DTGhSJTJCa01JUGJMJTJGVGFLcllxdTA4Q2tzMGpzOFY5VFFhSHlRcFpQeVNTa0N4dktDT3RTSzZleEZMbGZ1VHg1aThzWk91eEc1SjVCUDNDdHgzWkJVNXhOcWJQM2MwVEdndXRHSXJTJTJCTkRrRnlhZlltdktzMlZNVEw4MHMlMkJqV1Foeld1ek1BeldOQTlXWVZ3Q2dLNHZKSkdIVW5aNDFHV0dCU0lINlU4ZU8lMkJjJTNE',
        'cto_bidid': 'Wk7_2F9ZNE1VUHY2bEozZU4wRUpGeEw5TUs1OENsNklGWHVxUVFRT2h6ZGZ3TTV0M2FaeiUyQkJ3WXByV2lpbjlnbk1JdDVNd2NWMmZSaWJ1MTJ6OSUyRm9UVkRydWRBbWtwMzB1a21kZjhMOEFzJTJGeG1NTlhOMTdKTkRLclBzaVJjYWRVb2UyNWs4OTlQdkpWbkJ5MTRMNEszUVdZdEElM0QlM0Q',
        'OptanonAlertBoxClosed': '2023-01-05T01:51:28.348Z',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Jan+05+2023+09%3A51%3A49+GMT%2B0800+(%E4%B8%AD%E5%9B%BD%E6%A0%87%E5%87%86%E6%97%B6%E9%97%B4)&version=202211.2.0&isIABGlobal=false&hosts=&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=CN%3BSH',
    }

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh,en-US;q=0.9,en;q=0.8,zh-CN;q=0.7',
        'Connection': 'keep-alive',
        'If-None-Match': '"050abe5953f693b2d518444b68c200233-gzip"',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    r = requests.get(url, headers=headers)

    return r


def html_resolve(html):
    """
    对网页内容进行解析

    :param html: 网页原始文件
    """
    # entryContent
    # < div id = "entryContent" class ="oald" >

    # < div id = "ring-links-box" >

    soup = BeautifulSoup(html.text, 'html.parser')

    res = soup.find(id='entryContent')
    # print(res.find('h1').text.capitalize())
    try:
        print(res.find(class_="pos").text)
    except:
        print(res.find('h1').text, end='\t')
    res = res.find('ol')  # 提出idioms 习语
    word_sense = res.find_all(class_='sense')
    for i in word_sense:
        print('=' * 5)
        try:
            print('变体:', i.find(class_="variants").text)
        except:
            pass
        try:
            print('语法:', i.find(class_='grammar').text)
        except:
            pass
        try:
            print(f"用法:{i.find(class_='cf').text.strip()}", end="\t")
        except:
            pass

        print('释义:', i.find(class_='def').text)
        examples = i.find(class_='examples')
        print('用例:')
        try:
            for x in examples:
                try:
                    print(f"用法:{x.find(class_='cf').text.strip()}", end="\t")
                except:
                    pass
                print(x.find(class_='x').text.strip())
        except:
            pass
        # print('=' * 10)


# print(res.prettify())


def return_code(word='torpedo'):
    """
    判断html的返回值，如果出现定向跳转，说明单词有多个词性

    :param word: 查询的单词
    """
    r = get_html(word)

    if r.status_code == 404:
        print(f'{word} 单词不存在,可以尝试搜索 {word}1')
        # TODO 自动添加word1，测试搜索单词live
    elif not r.history:
        # print(r.status_code, r.url)
        print(word.capitalize())
        html_resolve(r)
    else:
        # print('多种词性')
        multi_attribute(word)


def multi_attribute(word):
    """
    单词有多个词性进行遍历

    :param word: 查询的单词
    """
    print(word.capitalize())
    for i in range(10):
        r = get_html(word + f'_{i + 1}')
        if r.status_code != 404:
            print('-' * 10)
            # print(r.status_code, r.url)
            html_resolve(r)

        else:
            break


if __name__ == '__main__':
    return_code(word='dick')
