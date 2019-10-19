# coding=utf-8
import sys
import json
from tqdm import tqdm
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import datetime

IS_PY3 = sys.version_info.major == 3
if IS_PY3:
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import URLError
    from urllib.parse import urlencode
    from urllib.parse import quote_plus
else:
    import urllib2
    from urllib import quote_plus
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import URLError
    from urllib import urlencode

API_KEY = 'wYPkr1BPcxfk60p80Gd0GCYy'
SECRET_KEY = 'H0m6fOQUrS4CsQxsZxl5v4seDflzlVzh'


# 发音人选择, 基础音库：0为度小美，1为度小宇，3为度逍遥，4为度丫丫，
# 精品音库：5为度小娇，103为度米朵，106为度博文，110为度小童，111为度小萌，默认为度小美
PER = 103
# 语速，取值0-15，默认为5中语速
SPD = 5
# 音调，取值0-15，默认为5中语调
PIT = 5
# 音量，取值0-9，默认为5中音量
VOL = 5
# 下载的文件格式, 3：mp3(default) 4： pcm-16k 5： pcm-8k 6. wav
AUE = 3

FORMATS = {3: "mp3", 4: "pcm", 5: "pcm", 6: "wav"}
FORMAT = FORMATS[AUE]

CUID = "123456PYTHON"

TTS_URL = 'http://tsn.baidu.com/text2audio'


class DemoError(Exception):
    pass


"""  TOKEN start """

TOKEN_URL = 'http://openapi.baidu.com/oauth/2.0/token'
SCOPE = 'audio_tts_post'  # 有此scope表示有tts能力，没有请在网页里勾选


def fetch_token():
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    post_data = urlencode(params)
    if (IS_PY3):
        post_data = post_data.encode('utf-8')
    req = Request(TOKEN_URL, post_data)
    try:
        f = urlopen(req, timeout=5)
        result_str = f.read()
    except URLError as err:
        print('token http response http code : ' + str(err.code))
        result_str = err.read()
    if (IS_PY3):
        result_str = result_str.decode()

    result = json.loads(result_str)
    if ('access_token' in result.keys() and 'scope' in result.keys()):
        if not SCOPE in result['scope'].split(' '):
            raise DemoError('scope is not correct')
        return result['access_token']
    else:
        raise DemoError('MAYBE API_KEY or SECRET_KEY not correct: access_token or scope not found in token response')


"""  TOKEN end """


def run_tts(TEXT, serial_no, input_file_path):
    token = fetch_token()
    tex = quote_plus(TEXT)  # 此处TEXT需要两次urlencode
    params = {'tok': token, 'tex': tex, 'per': PER, 'spd': SPD, 'pit': PIT, 'vol': VOL, 'aue': AUE, 'cuid': CUID,
              'lan': 'zh', 'ctp': 1}  # lan ctp 固定参数

    data = urlencode(params)

    req = Request(TTS_URL, data.encode('utf-8'))
    has_error = False
    try:
        f = urlopen(req)
        result_str = f.read()

        headers = dict((name.lower(), value) for name, value in f.headers.items())

        has_error = ('content-type' not in headers.keys() or headers['content-type'].find('audio/') < 0)
    except URLError as err:
        print('asr http response http code : ' + str(err.code))
        result_str = err.read()
        has_error = True

    save_file = "error.txt" if has_error else 'result.' + FORMAT

    audio_name_prefix = os.path.basename(os.path.dirname(input_file_path))
    audio_output_path = os.path.join(os.path.dirname(input_file_path), audio_name_prefix)
    try:
        os.mkdir(audio_output_path)
    except:
        pass
    save_file = os.path.join(audio_output_path, '{}-{}.mp3'.format(audio_name_prefix, serial_no))

    # txt_path = os.path.join(audio_output_path, '{}-{}.txt'.format(audio_name_prefix, serial_no))
    # with open(txt_path, 'w', encoding='utf-8') as f:
    # f.write(TEXT)

    with open(save_file, 'wb') as of:
        of.write(result_str)

    if has_error:
        if (IS_PY3):
            result_str = str(result_str, 'utf-8')
        print("tts api  error:" + result_str)


def text_byte_num_cut(text, byte_limit):
    split_text_list = []
    single_text = ''
    for char_ in text:
        if len((single_text+char_).encode('utf-8')) >= byte_limit:
            split_text_list.append(single_text)
            single_text = ''
        single_text += char_
    split_text_list.append(single_text)
    return split_text_list


if __name__ == "__main__":
    txt_file_path = r"E:\python\python-post-tencent\PDF\吴仁华：天安门血腥清场内幕\ocr_result.txt"
    #  待合成文本内容
    with open(txt_file_path, 'r', encoding='utf-8') as f:
        text = f.read().replace('\n', "")
    print('总字数：', len(text))
    text_list = text_byte_num_cut(text, 2040)
    print('分段数：', len(text_list))

    # for i, text in enumerate(tqdm(text_list)):
    #     run_tts(text, i, txt_file_path)

    with ThreadPoolExecutor(max_workers=3) as exe:
        future_list = [exe.submit(run_tts, text, i, txt_file_path) for i, text in enumerate(text_list)]
        completed_task_count = 0
        start_time = datetime.datetime.now()
        for future in as_completed(future_list):
            completed_task_count += 1
            complete_rate = completed_task_count/len(future_list)
            past_seconds = (datetime.datetime.now() - start_time).seconds
            estimate_seconds = past_seconds/complete_rate
            remaining_seconds = int(estimate_seconds-past_seconds)
            print(datetime.datetime.now().strftime('%F %X') + ' Progress: '+str(int(complete_rate*100))+'%, runing {}m{}s, remain {}m{}s...'.format(past_seconds//60, past_seconds % 60, remaining_seconds//60, remaining_seconds % 60))