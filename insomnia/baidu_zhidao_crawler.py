#_-*-coding:utf-8-*-

from bs4 import BeautifulSoup
import requests
import re

session = requests.session()
session.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'


def truncate_txt(path):
    with open(path, 'r+', encoding='utf-8') as f:
        f.truncate()

def get_urls(url_head, page_num):
    # 爬取百度知道所有关于“思诺思”的问答结果
    url_list = []
    for page_i in range(0, page_num):
        print('----------------------------------正在爬第{}页---------------------------------'.format(str(page_i+1)))
        # 百度知道搜索关键字为“思诺思 失眠”的搜索结果
        org_url = url_head + str(page_i*10)
        soup = get_html(org_url)
        dts = soup.find_all('dt', attrs={'class': 'dt mb-4 line'})
        for dt in dts:
            url_list.append(dt.a['href'])
            print(dt.a['href'])
    return url_list

def get_html(url):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'BAIDUID=21B21471EA89B20710211D16D0F35CA3:FG=1; BIDUPSID=21B21471EA89B20710211D16D0F35CA3; PSTM=1506835500; BDUSS=zZDMFphMWZ-M2dafmZsakJVeTh3OE03YzU2Z04zQ0hCcGZUSGxXV1VhRloyRjVhQVFBQUFBJCQAAAAAAAAAAAEAAABOGsUYtXTM7wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAFlLN1pZSzdaU; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; H_PS_PSSID=1425_25809_21114_18559_27153; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; delPer=0; PSINO=1; IKUT=1683; ZD_ENTRY=baidu; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1540814390,1540814497,1540814623,1540869599; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1540869844; PMS_JT=%28%7B%22s%22%3A1540870136519%2C%22r%22%3A%22https%3A//zhidao.baidu.com/search%3Fword%3D%25CB%25BC%25C5%25B5%25CB%25BC+%25CA%25A7%25C3%25DF%26ie%3Dgbk%26site%3D-1%26sites%3D0%26date%3D0%26pn%3D140%22%7D%29',
        'Host': 'zhidao.baidu.com',
        # 'Referer': 'https://zhidao.baidu.com/search?word=%CB%BC%C5%B5%CB%BC+%CA%A7%C3%DF&ie=gbk&site=-1&sites=0&date=0&pn=140',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'    }
    try:
        r = session.get(url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        return soup
    except Exception as e:
        # raise
        pass
    finally:
        pass

def get_content(soup):
    content = ' '
    if soup:
        ask_title = soup.find_all('span', class_='ask-title')
        ask_con = soup.find_all('span', class_='con-all')
        best_answer = soup.find_all('div', class_='best-text mb-10')
        answers = soup.find_all('div', class_='answer-text mb-10 line')
        for title in ask_title:
            content += title.string
        for conn in ask_con:
            content += str(conn)
        for best in best_answer:
            content += str(best)
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
    url_head1 = 'https://zhidao.baidu.com/search?word=%CB%BC%C5%B5%CB%BC+%CA%A7%C3%DF&ie=gbk&site=-1&sites=0&date=0&pn='
    url_list1 = get_urls(url_head1, 18)
    # 搜索关键词为“唑吡坦 失眠”
    url_head2 = 'https://zhidao.baidu.com/search?word=%DF%F2%DF%C1%CC%B9+%CA%A7%C3%DF&ie=gbk&site=-1&sites=0&date=0&pn='
    url_list2 = get_urls(url_head2, 24)

    url_path = 'html_urls/baidu_zhidao_urls.txt'    # url存入txt
    output_path = 'result/baidu_zhidao_corpus.txt'      # 结果写入txt
    truncate_txt(url_path)
    truncate_txt(output_path)

    for url in set(url_list1 + url_list2):
        print(url)
        write_to_txt(url_path, str(url)+'\n')
        soup = get_html(url)
        content = get_content(soup)
        filter_content = get_filter_content(content)
        write_to_txt(output_path, filter_content)

if __name__ == '__main__':
    main()
