import requests
from bs4 import BeautifulSoup

def get_html(url):
    headers = {
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'jsluid=8628301f6a80d5bf23501a15877304d5; UM_distinctid=1669f7073d94c0-01d9ca39cfb70a-b79193d-1fa400-1669f7073da2c9; CNZZDATA30036369=cnzz_eid%3D1992382279-1540270669-null%26ntime%3D1540270669; drug_ids=a%3A1%3A%7Bi%3A0%3Bi%3A22637%3B%7D; Hm_lvt_7c2c4ab8a1436c0f67383fe9417819b7=1540273239; Hm_lpvt_7c2c4ab8a1436c0f67383fe9417819b7=1540273782; cn_30036369_dplus=%7B%22distinct_id%22%3A%20%221669f7073d94c0-01d9ca39cfb70a-b79193d-1fa400-1669f7073da2c9%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201540274010%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201540274010%7D%7D',
        'Host': 'yp.120ask.com',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    try:
        html = requests.get(url, headers=headers, timeout=5)#请求超过5秒，报错。设置响应时间
        soup=BeautifulSoup(html.content, 'lxml')
        return soup
    except Exception as e:
        raise   # raise提取出错误，中断程序
    finally:
        pass

def get_content(soup):
    drugDes = soup.find_all('div', class_='drugDecri')[0]
    drugInfo = drugDes.find_all('p', class_='clears')
    print(drugInfo)
    content = ''
    for i in range(len(drugInfo)):
        content += str(drugInfo[i].span.string) + ' ' + str(drugInfo[i].var.string)+'\n'
    return content

def write_to_txt(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    # 爬取思诺思产品说明书
    url = 'http://yp.120ask.com/manual/22637.html'
    soup = get_html(url)
    content = get_content(soup)
    path = 'result/product_sys.txt'
    write_to_txt(path, content)

if __name__ == '__main__':
    main()