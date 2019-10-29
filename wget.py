import requests
from tqdm import tqdm
import os
import sys
from retrying import retry


@retry(wait_fixed=10000, stop_max_attempt_number=6)
def download(url_txt_path, use_proxies, download_folder_path, url, proxies, headers):
    if use_proxies == '1':
        response = requests.get(url, headers=headers, proxies=proxies)
    elif use_proxies == '0':
        response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(url, '下载失败', response.status_code)
        with open('_downloading_log'.join(os.path.splitext(url_txt_path)), 'a', encoding='utf-8') as f:
            f.write(url + '\t下载失败' + '\n')
        return
    content = response.content
    with open(os.path.join(download_folder_path, url.split('/')[-1]), 'wb') as f:
        f.write(content)


def wget(url_txt_path, use_proxies='0', download_folder_path=None):
    if download_folder_path is None:
        download_folder_path = os.path.dirname(url_txt_path)
    proxies = {
        "http": "socks5://127.0.0.1:1080",
        'https': 'socks5://127.0.0.1:1080'
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }

    with open(url_txt_path, 'r', encoding='utf-8') as f:
        url_list = f.read().split('\n')

    for url in tqdm(url_list):
        download(url_txt_path, use_proxies, download_folder_path, url, proxies, headers)


if __name__ == "__main__":
    if len(sys.argv) == 4:
        wget(sys.argv[1], sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        wget(sys.argv[1], sys.argv[2])
    elif len(sys.argv) == 2:
        wget(sys.argv[1])
    else:
        print('args : url_txt_path, use_proxies=0, download_folder_path=None')
