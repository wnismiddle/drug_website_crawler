# -*- coding:utf-8 -*-

import re
# from HTMLParser import HTMLParser
import requests
from bs4 import BeautifulSoup
import re

def get_urls():
    url_list = []
    # 爬取39健康网上和思诺思相关的所有问答对
    for i in range(1, 8):
        print('----------------------------------正在爬第{}页---------------------------------'.format(str(i)))
        ori_url = 'http://ask.39.net/browse/319753712-1-' + str(i) +'.html'
        soup = get_html(ori_url)
        ask_tiles = soup.find_all('p', class_='question-ask-title')

        url_head = 'http://ask.39.net'
        for title in ask_tiles:
            url_list.append(url_head + title.a['href'])
            print(url_head + title.a['href'])
    return url_list

def get_html(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'Hm_lvt_9840601cb51320c55bca4fa0f4949efe=1540274320; _ga=GA1.2.1231127461.1540274324; _39wt_pk_cookie=53b94851d360c12cedb5ea202fae39e8-1435040853; _39wt_session_cookie=8e2fb772c5c2a76bbee31e187e52e6de-1435040853; _39wt_last_session_cookie=8e2fb772c5c2a76bbee31e187e52e6de-1435040853; _39wt_site_refer_server_cookie=so.39.net; _39wt_session_refer_cookie=http%253A%252F%252Fso.39.net%252Fs%253Fwords%253D%2525u5931%2525u7720; area_info=CN320000|%D6%D0%B9%FA|%BD%AD%CB%D5|-|%D2%C6%B6%AF; Hm_lvt_ab2e5965345c61109c5e97c34de8026a=1540274304,1540277442; Hm_lpvt_ab2e5965345c61109c5e97c34de8026a=1540277442; _39wt_site_refer_url_md5_cookie=e4e5eddb254a644527f18fb7539228b0; _gat=1; JSESSIONID=1FBDC8E7ECBB5FA498468A23C80FEDE4; Hm_lpvt_9840601cb51320c55bca4fa0f4949efe=1540277502; Hm_lvt_6e8573fc07ff21285f41cba3fb1618af=1540277458,1540277478,1540277491,1540277504; Hm_lpvt_6e8573fc07ff21285f41cba3fb1618af=1540277504; Hm_lvt_4b568bfb716f2b26c619470ea3189b1a=1540277504; Hm_lpvt_4b568bfb716f2b26c619470ea3189b1a=1540277504; _39wt_last_visit_time_cookie=1540277503824',
        'Host': 'ask.39.net',
        'Referer': 'http://so.39.net/s?words=%u601D%u8BFA%u601D',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'lxml')
        return soup
    except Exception as e:
        raise   # raise提取出错误，中断程序
    finally:
        pass

def get_content(soup):
    answers = soup.find_all('p', class_='sele_txt')
    cotent = ''
    ask_title = soup.find_all('p', class_='ask_tit')[0]     # 患者问题
    ask_supple = soup.find_all('p', class_='txt_ms')[0]     # 患者问题详细描述
    cotent += str(ask_title)
    cotent += str(ask_supple)
    # 医生回答
    for a in answers:
        print(a)
        cotent += str(a)
    return cotent

# 清空txt
def truncate_txt(path):
    with open(path, 'r+', encoding='utf-8') as f:
        f.truncate()

# 爬取结果追加写入txt
def write_to_txt(path, content):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content)

def get_filter_content(content):
    #将所有html标签替换成换行符
    # content = str(content).replace('<br/>', '')
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('\n', content)
    return dd

def main():
    url_list = get_urls()
    # url_list = ["http://ask.39.net/question/39134222.html", ]

    url_path = 'html_urls/120ask_urls.txt'     # url存入txt
    output_path = 'result/999corpus.txt'    # 结果写入txt
    truncate_txt(url_path)
    truncate_txt(output_path)

    for url in url_list:
        print(url)
        write_to_txt(url_path, str(url)+'\n')
        soup = get_html(url)
        content = get_content(soup)
        filter_content = get_filter_content(content)
        write_to_txt(output_path, filter_content)

if __name__ == '__main__':
    main()