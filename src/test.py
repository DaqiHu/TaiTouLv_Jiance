import requests
from lxml import html
import os
from urllib.parse import urljoin

def parse_and_download(url):
    # 发送HTTP请求获取网页内容
    response = requests.get(url)
    # 解析HTML内容
    tree = html.fromstring(response.content)
    # 使用XPath提取链接
    links = tree.xpath('//a/@href')
    # 打印链接并下载文件
    for link in links:
        print("Link:", link)
        if link.endswith('.jpg'):  # 只下载PDF文件，你可以根据需要修改条件
            file_url = urljoin(url, link)
            file_name = os.path.join("downloads", file_url.split('/')[-1])
            with requests.get(file_url, stream=True) as r:
                r.raise_for_status()
                with open(file_name, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)

if __name__ == "__main__":
    url = "https://book.douban.com"  # 替换成你想要解析的网页URL
    parse_and_download(url)
