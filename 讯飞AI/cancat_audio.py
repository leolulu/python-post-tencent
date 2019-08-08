import os
from pydub import AudioSegment
from functools import reduce
import numpy as np
from tqdm import tqdm

folder_path = r'E:\python\python-post-tencent\讯飞AI\audio\数据挖掘导论'
inner_folder_path = older_path, os.path.basename(folder_path)
try:
    os.makedirs(inner_folder_path)
except:
    pass

path_list = [os.path.join(folder_path, i) for i in os.listdir(folder_path)]
path_list.sort(key=lambda x: os.path.basename(x).split('.')[0].zfill(5))
path_list = np.array_split(path_list, int(len(path_list)/10))

for i, every_list_part in enumerate(tqdm(path_list)):
    audio_list = map(lambda x: AudioSegment.from_wav(x), every_list_part)
    reduce(lambda x, y: x+y, audio_list).export(os.path.join(inner_folder_path, 'concat_audio_{}.mp3'.format(i)), format='mp3')
