import requests
import json
import base64
import re
import os
from tqdm import tqdm_notebook,tqdm


def ocr_high_precision(folder_path):

    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=0NYQV12ICQHdz7GurbrzcgEL&client_secret=VOGmWvIkYrXc5Hfx8Q4SIH504Ku0PPWU'
    url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=' + json.loads(requests.post(host).content)['access_token']

    def get_ocr_reslut(image_path):
        with open(image_path, 'rb') as f:
            img = base64.b64encode(f.read())
            params = {"image": img}
        return ''.join([i['words'] for i in json.loads(requests.post(url, data=params).content)['words_result']])

    pic_path_list = [os.path.join(folder_path, i) for i in os.listdir(folder_path)]
    pic_path_list.sort(key=lambda x: os.path.basename(x).split('.')[0].split('_')[-1].zfill(5))

    for pic_path in tqdm(pic_path_list):
        with open(os.path.join(os.path.dirname(folder_path), f'{os.path.basename(folder_path)}_ocr_result.txt'), 'a', encoding='utf-8') as f:
            f.write(get_ocr_reslut(pic_path)+'\n')


if __name__ == "__main__":
    ocr_high_precision(r'E:\裏\图\OneDrive - Office.Inc\多模态处理文件夹\贫穷的本质\《贫穷的本质：我们为什么摆脱不了贫穷》_image')