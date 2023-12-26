# VoiveRobot
机器人语音小助手

1、ROS安装：作者使用鱼香ROS进行安装，其地址链接为https://fishros.org.cn/forum/topic/20/%E5%B0%8F%E9%B1%BC%E7%9A%84%E4%B8%80%E9%94%AE%E5%AE%89%E8%A3%85%E7%B3%BB%E5%88%97?lang=zh-CN。（作者使用的是noetic版本,ubuntu20.04）

一键安装的脚本如下：

```
wget http://fishros.com/install -O fishros && . fishros
```

2、edge-tts安装：edge-tts微软文本转语音库，支持文本转语音，同时也支持使用不同的口音播报。

安装的命令如下：

```
pip install edge-tts
edge-tts --list-voices --可以查看支持的语音
edge-tts --voice zh-CN-YunxiNeural --text "hello World" --write-media hello_world.mp3 --添加--voice命令，指定输出的语音。
--rate与--volume用于调整语速与音量
```

3、playsound安装：用于播报语音文件。

安装的命令如下：

```
pip install playsound
--基本用法：
from playsound import playsound  
playsound('your_voice.mp3')  
```

4、百度应用创建：

需要去百度智能云平台创建相应的应用才能够使用，其地址为：https://console.bce.baidu.com/

