import os
import subprocess

# Python中使用Shell命令
# e.g., 使用ffmpeg转换视频

audio_aac_path = os.path.join(tmp_path, f'{video_filename}.aac')
audio_wav_path = os.path.join(tmp_path, f'{video_filename}.wav')

# 传递参数
mp4_to_acc = f'{which_ffmpeg()} -hide_banner -loglevel panic -y -i {video_path} -acodec copy {audio_aac_path}'
aac_to_wav = f'{which_ffmpeg()} -hide_banner -loglevel panic -y -i {audio_aac_path} {audio_wav_path}'
subprocess.call(mp4_to_acc.split())
subprocess.call(aac_to_wav.split())

# e.g., 使用shutil进行文件的复制，转换
