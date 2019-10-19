import os
from pydub import AudioSegment
from functools import reduce
import numpy as np
from tqdm import tqdm


folder_path = r'E:\python\python-post-tencent\PDF\精要主义\精要主义'
cancat_num = 5

title_name = os.path.basename(folder_path)
path_list = [os.path.join(folder_path, i) for i in os.listdir(folder_path) if os.path.splitext(i)[-1] == '.wav']
path_list.sort(key=lambda x: os.path.basename(x).split('.')[0].split('-')[-1].zfill(5))
path_list = np.array_split(path_list, int(len(path_list)/cancat_num) if len(path_list) >= cancat_num else 1)

inner_folder_path = os.path.join(folder_path, title_name+'_合并音频')
try:
    os.makedirs(inner_folder_path)
except:
    pass

for i, every_list_part in enumerate(tqdm(path_list)):
    audio_list = map(lambda x: AudioSegment.from_wav(x), every_list_part)
    reduce(lambda x, y: x+y, audio_list).export(os.path.join(inner_folder_path, '{}_concat_audio_{}.mp3'.format(title_name, i)), format='mp3')
