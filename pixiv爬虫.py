import requests
from lxml import etree
from retrying import retry

page_num = 1
headers = {
    "Cookie": "vote=1; __utmz=20658210.1460984814.55.2.utmcsr=konachan.com|utmccn=(referral)|utmcmd=referral|utmcct=/post/switch; __cfduid=d18af1d27bb5882a6eff521053cb3cc801525011444; tag-script=; country=US; blacklisted_tags=%5B%22%22%5D; konachan.net=BAh7B0kiD3Nlc3Npb25faWQGOgZFVEkiJTlhYTcwNjk4YzI4NjdjYWU2YjZhYzg2YTZiOWRlZmQ1BjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMTIxZXdwajVzYVRuR0huSWtWWEUrdlJPOE1EMUdCMHdUdG5yMjFXNmNVNm89BjsARg%3D%3D--8a1e71bdae987934cb60ab31c927084b3c5d85c6; __utmc=20658210; Hm_lvt_ba7c84ce230944c13900faeba642b2b4=1536069861,1536796970,1536939737,1537279770; __utma=20658210.97867196.1446035811.1537370253.1537509624.843; __utmt=1; forum_post_last_read_at=%222018-09-21T08%3A00%3A31%2B02%3A00%22; __utmb=20658210.3.10.1537509624; Hm_lpvt_ba7c84ce230944c13900faeba642b2b4=1537509630",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,zh-TW;q=0.6"
}
proxies = {
    "http": "socks5://127.0.0.1:1080",
    'https': 'socks5://127.0.0.1:1080'
}
session = requests.session()


@retry(stop_max_attempt_number=6, stop_max_delay=5000)
def recursionNextpage(url):
    global page_num
    r = session.get(url, headers=headers, proxies=proxies)
    html = etree.HTML(r.content)
    next_page_url = html.xpath(r"//a[@class='next']/@href")
    last_date = html.xpath(r"//time/text()")[-1]
    print('{}-{}'.format(page_num, last_date))

    title_list = html.xpath(r"//h2[@class='arc__title ']/a/text()")
    title_url_list = ['https://www.pixivision.net' + i for i in html.xpath(r"//h2[@class='arc__title ']/a/@href")]
    for title, title_url in zip(title_list, title_url_list):
        with open('./pixivision_titles.txt', 'a', encoding='utf-8') as f:
            f.write('{}\t{}\t{}\n'.format(page_num, title, title_url))
    page_num += 1

    if len(next_page_url) > 0:
        next_page_url = "https://www.pixivision.net" + next_page_url[0]
        recursionNextpage(next_page_url)


recursionNextpage('https://www.pixivision.net/zh/c/illustration')
