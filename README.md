# VoiveRobot
机器人语音小助手

1、ROS安装：作者使用鱼香ROS进行安装，其地址链接为https://fishros.org.cn/forum/topic/20/%E5%B0%8F%E9%B1%BC%E7%9A%84%E4%B8%80%E9%94%AE%E5%AE%89%E8%A3%85%E7%B3%BB%E5%88%97?lang=zh-CN。（作者使用的是noetic版本,ubuntu20.04）

一键安装的脚本如下:

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

5、action.py主要用于定义机器人运动相关的函数，作者已经在里边定义了一些常见的机器人动作函数，比如：机器人前进、后退、左转、右转以及运动多少时间等。
这一块是存在一定的局限的，就是需要提前定义好相关的函数，未来的改进可能会是通过输入的指令，让大模型自动生成相应的代码并执行，这就在一定程度上提高了
机器人的智能化程度。此外、这一块的代码是可以被迁移到其他的机器人平台上的，作者的应用场景主要是在巡检机器人上，其他的平台类似于：机械臂、无人机等也是
可以运用的。

