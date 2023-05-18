# Useful Shell Scripts
In fact, many tasks could be finished easily by using the shell scripts. 
## Video processing
This part is mainly built based on the ffmpeg commands. For more info, please refer to the [ffmpeg](https://github.com/FFmpeg/FFmpeg),
and there are very amount of open repos on the github website. However, for the convinience, I record some commands and scripts for reference.

### FFMPEG
- 将一个文件夹中的所有帧，生成一个视频
```
cd $folder_file
ffmpeg -framerate 30 -pattern_type glob -i '*.png' -i audio.ogg -c:a copy -shortest -c:v libx264 -pix_fmt yuv420p out.mp4
```

