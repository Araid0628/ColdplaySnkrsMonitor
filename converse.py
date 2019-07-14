import requests
from lxml import html
import re
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import urllib.request

# //*[@id="sku-product-list"]/dl[1]
# 女鞋 https://www.converse.com.cn/allstar/category.htm?iid=npkvnv070120191000
# 男鞋 https://www.converse.com.cn/men/category.htm?iid=tpnvmc0601201501
# 165421c


def get_url():
    url = "https://www.converse.com.cn/allstar/category.htm?iid=npkvnv070120191000"
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}
    req = urllib.request.Request(url)
    webpage = urllib.request.urlopen(req)
    html = webpage.read()
    soup = BeautifulSoup(html, 'html.parser')
    list = []
    for k in soup.find_all('a'):
        # print(k.get('href'))
        list.append(k.get('href'))
        # if '564981C' in k['href']:
        #     print(k)
        #     print(k.get('href'))  # 查a标签的href值
    for _ in list:
        if '165421c' in _:
            return _
        else:
            return None


print(get_url())
