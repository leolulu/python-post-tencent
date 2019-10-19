import wave
import os
import sys
import subprocess
from concurrent.futures import ProcessPoolExecutor


def pcm2wav(pcm_path):
    wav_path = os.path.splitext(pcm_path)[0]+'.wav'
    with open(pcm_path, 'rb') as pcmfile:
        pcmdata = pcmfile.read()
    with wave.open(wav_path, 'wb') as wavfile:
        wavfile.setparams((1, 2, 16000, 0, 'NONE', 'NONE'))
        wavfile.writeframes(pcmdata)


def wav2mp3(wav_path):
    mp3_path = os.path.splitext(wav_path)[0]+'.mp3'
    subprocess.call(f'ffmpeg -i {wav_path} {mp3_path}', shell=True)


def wav2mp3_whole_folder_convert(wav_folder_path):
    wav_file_path_list = [os.path.join(wav_folder_path, i) for i in os.listdir(wav_folder_path) if os.path.splitext(i)[-1] == '.wav']
    with ProcessPoolExecutor(4) as exe:
        for wav_file_path in wav_file_path_list:
            exe.submit(wav2mp3, wav_file_path)


if __name__ == "__main__":
    pcm2wav(sys.argv[1])
