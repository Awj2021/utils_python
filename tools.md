# Common Modules Commands Usage
## os
> os.path
```
os.path.abspath(path)  # 返回绝对路径
os.path.split(path)    # 路径分割(目录和文件名的二元组)
os.path.dirname(path)  # 返回path的目录层的路径
os.path.basename(path) # path最后的文件名
os.path.isfile(path)   # path文件存在，return True; 否则：false
os.path.isdir(path)    # path是存在的目录，return True; otherwise, false
os.path.splitext(path) # 分离文件名与扩展名,e.g., /home/ai.png -> '/home/ai' 'png'
```