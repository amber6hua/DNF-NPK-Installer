# DNF补丁安装器

## 前言

> 以前对替换补丁很热衷。但是找了一大堆补丁放进去，很多失效的，补丁一多，找出来又很麻烦。
> 最近回坑了，突然想做个管理补丁的程序。
> 把所有补丁放到同一个目录下管理，然后通过程序，统一追加删除。

## 使用环境
> Win10 Win11 其他没试过

## 使用说明
- 启动exe文件，出现操作界面
- 初次启动时，选择文件夹，设置存放补丁的公共目录
- 配置保存在config.ini
- 把单个补丁文件放入公共目录，也可以把一套补丁整理成一个文件夹后放入公共目录
- 重启或者重新选择npk目录后，放入的补丁才会加载出来
- 设置dnf中的目录（设置自己的dnf目录下的ImagePacks2也可以设置SoundPack）
- 在左边的列表框选择要安装的补丁，点击安装
- 在右边的列表框选择要卸载的补丁，点击卸载

## 额外
- 如果想替换语音补丁，可以选择设置的SoundPacks，存放补丁的公共目录，只存放语音补丁，别混起来。
- 可以复制项目文件夹，一个用来管理 ImagePacks2的贴图 一个用来管理 SoundPacks的语音，完美。

## 注意：

- 该项目本质是把，补丁追加到ImagePacks2下，即同名文件会跳过，不会替换覆盖原本的NPK文件 
- 支持次级目录，即 可以把一套补丁，放在同一个目录下，再放到公共目录下
    安装时就能把一套补丁，一起安装。 
- 如果是和源文件同名，必须替换的补丁，建议自己手动替换。（强迫症不喜欢动源文件）

## pyinstaller 打包

> 打包成exe,没有python环境也能运行

```bash
# 安装 pyinstaller
pip install pyinstaller

# 利用pyinstaller 把main.py 打包成exe win可执行文件
pyinstaller -F -w main.py
```

## 预览图

主界面
![image](https://cdn.staticaly.com/gh/amber6hua/cdn@master/image-hosting/image.sly72eg8x0w.webp)

存放补丁的示例
![image](https://cdn.staticaly.com/gh/amber6hua/cdn@master/image-hosting/image.sly72eg8x0w.webp)

![image](https://cdn.staticaly.com/gh/amber6hua/cdn@master/image-hosting/image.sly72eg8x0w.webp)