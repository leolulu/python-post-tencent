import wave
import os
import sys
import subprocess
from concurrent.futures import ProcessPoolExecutor
import shutil


def pcm2wav(pcm_path):
    wav_path = os.path.splitext(pcm_path)[0]+'.wav'
    with open(pcm_path, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    with wave.open(wav_path, 'wb') as wavfile:
        wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)


def wav2mp3(wav_path):
    mp3_path = os.path.splitext(wav_path)[0]+'.mp3'
    subprocess.call(f'ffmpeg -i "{wav_path}" "{mp3_path}"', shell=True)


def wav2mp3_whole_folder_convert(wav_folder_path):
    wav_file_path_list = [os.path.join(wav_folder_path, i) for i in os.listdir(wav_folder_path) if os.path.splitext(i)[-1] == '.wav']
    with ProcessPoolExecutor(4) as exe:
        for wav_file_path in wav_file_path_list:
            exe.submit(wav2mp3, wav_file_path)
    return wav_file_path_list


def wav2mp3_whole_folder_convert_with_file_move(wav_folder_path):
    wav_file_path_list = wav2mp3_whole_folder_convert(wav_folder_path)
    txt_file_path_list = [os.path.join(wav_folder_path, i) for i in os.listdir(wav_folder_path) if os.path.splitext(i)[-1] == '.txt']

    wav_store_folder = os.path.join(wav_folder_path, 'WAV')
    txt_store_folder = os.path.join(wav_folder_path, 'TXT')
    [os.mkdir(i) for i in [wav_store_folder, txt_store_folder]]
    [shutil.move(i, wav_store_folder) for i in wav_file_path_list]
    [shutil.move(i, txt_store_folder) for i in txt_file_path_list]


if __name__ == "__main__":
    wav2mp3_whole_folder_convert_with_file_move(r'E:\裏\图\OneDrive - Office.Inc\多模态处理文件夹\贫穷的本质\贫穷的本质_audio')