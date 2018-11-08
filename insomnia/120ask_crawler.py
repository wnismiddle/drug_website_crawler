#_-*-coding:utf-8-*-

from bs4 import BeautifulSoup
import requests
import re
import os
import json
import time

session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'


def truncate_txt(path):
    if not os.path.exists(path):
        return
    with open(path, 'r+', encoding='utf-8') as f:
        f.truncate()

def get_urls(url_head, page_num):
    headers = {
        'Referer': 'http://so.120ask.com/?kw=%E6%80%9D%E8%AF%BA%E6%80%9D+%E5%A4%B1%E7%9C%A0&nsid=1&page=3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
    }
    url_list = []
    for page_i in range(0, page_num):
        print('----------------------------------正在爬第{}页---------------------------------'.format(str(page_i+1)))
        org_url = url_head + str(page_i)
        try:
            r = session.get(org_url, headers=headers)
            print(r.content)
            pattern = re.compile(r'[(](.*)[)]', re.S)
            data = re.findall(pattern, str(r.content))[0]
            if data:
                data = json.loads(data)
                for i in range(len(data['blockData'])):
                    url = str(data['blockData'][i]['linkurl'])
                    url_list.append(url.replace('\\', ''))
                    print(url.replace('\\', ''))
        except Exception as e:
            raise
        finally:
            pass
    return url_list

def get_html(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': '__jsluid=4cb1c0776cb1a8280cc733f7e6a85b5d; UM_distinctid=1669f7073d94c0-01d9ca39cfb70a-b79193d-1fa400-1669f7073da2c9; cn_30036369_dplus=%7B%22distinct_id%22%3A%20%221669f7073d94c0-01d9ca39cfb70a-b79193d-1fa400-1669f7073da2c9%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201540277448%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201540277448%7D%7D; comHealthCloudUserProfileUseTag=49ec3149d6d73087a70cf11ba5e22308; TUSHENGSID=TS1540947897051; Hm_lvt_7c2c4ab8a1436c0f67383fe9417819b7=1540273239,1540947897,1540950763; CNZZDATA30036369=cnzz_eid%3D1270018442-1540945457-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1540950007; page_keyword=%E5%90%83%E6%80%9D%E8%AF%BA%E6%80%9D10MG%E5%8D%8A%E5%B9%B4%E7%AA%81%E7%84%B6%E5%81%9C%E4%BA%86%E4%BC%9A%E6%80%8E%E4%B9%88%E6%A0%B7; Hm_lpvt_7c2c4ab8a1436c0f67383fe9417819b7=1540954802',
        'Host': 'www.120ask.com',
        'Referer': 'http://so.120ask.com/?kw=%E6%80%9D%E8%AF%BA%E6%80%9D+%E5%A4%B1%E7%9C%A0&nsid=1&page=10',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
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
    content = ' '
    if soup:
        ask_title = soup.find_all('h1', id_='ask-d_askH1')
        ask_con = soup.find_all('div', class_='b_askcont')
        answers = soup.find_all('div', class_='b_anscont_cont')
        for title in ask_title:
            content += title.string
        for conn in ask_con:
            content += str(conn)
        for answer in answers:
            content += str(answer)
    print(content)
    return content

def get_filter_content(content):
    #将所有html标签替换成换行符
    # content = str(content).replace('<br/>', '')
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('\n', content)
    return dd

def write_to_txt(path, content):
    with open(path, 'a', encoding='utf-8') as f:
        f.write(content)

def main():
    # 搜索关键词为“思诺思 失眠”
    url_list1 = []
    url_head1 = 'http://zhannei.baidu.com/api/customsearch/apisearch?s=8725790603301206127&q=%E6%80%9D%E8%AF%BA%E6%80%9D%20%E5%A4%B1%E7%9C%A0&nojc=1&ct=2&cc=www.120ask.com&tk=3831311f25685e024c52887b6bda5330&v=2.0&callback=flyjsonp_FA118F5D60414A21881E84D101982A5A&p='
    url_list1 = get_urls(url_head1, 76)
    # # 搜索关键词为“唑吡坦 失眠”
    url_list2 = []
    url_head2 = 'http://zhannei.baidu.com/api/customsearch/apisearch?s=8725790603301206127&q=%E5%94%91%E5%90%A1%E5%9D%A6%20%E5%A4%B1%E7%9C%A0&nojc=1&ct=2&cc=www.120ask.com&tk=3831311f25685e024c52887b6bda5330&v=2.0&callback=flyjsonp_00867FF1FEC943EC85E61CDDE1D89467&p='
    url_list2 = get_urls(url_head2, 76)

    url_path = 'html_urls/120ask_urls.txt'  # url存入txt
    output_path = 'result/120ask_crawler.txt'   # 爬取结果写入txt
    truncate_txt(url_path)
    truncate_txt(output_path)

    for url in set(url_list1 + url_list2):
        print(url)
        write_to_txt(url_path, str(url)+'\n')
        soup = get_html(url)
        content = get_content(soup)
        filter_content = get_filter_content(content)
        write_to_txt(output_path, filter_content)

def addictive_crawler():
    # 搜索关键词为“思诺思 上瘾”
    url_list = []
    url_head = 'http://zhannei.baidu.com/api/customsearch/apisearch?s=8725790603301206127&q=%E6%80%9D%E8%AF%BA%E6%80%9D%20%E4%B8%8A%E7%98%BE&nojc=1&ct=2&cc=www.120ask.com&tk=3831311f25685e024c52887b6bda5330&v=2.0&callback=flyjsonp_136E380E24C447BB990A19A73AAA5DF0&p='
    url_list = get_urls(url_head, 2)

    url_path = 'html_urls/120ask_addictive_urls.txt'  # url存入txt
    output_path = 'result/120ask_addictive_crawler.txt'   # 爬取结果写入txt
    truncate_txt(url_path)
    truncate_txt(output_path)

    for url in set(url_list):
        print(url)
        write_to_txt(url_path, str(url)+'\n')
        soup = get_html(url)
        content = get_content(soup)
        filter_content = get_filter_content(content)
        write_to_txt(output_path, filter_content)

if __name__ == '__main__':
    start_time = time.time()
    addictive_crawler()
    end_time = time.time()
    print('cost time:{}s'.format(end_time-start_time))
