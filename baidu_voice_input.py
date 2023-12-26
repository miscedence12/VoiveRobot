
import requests
import json
import base64
import pyaudio
import wave
import os
import psutil
import sys
API_KEY = ' ' #API KEY
SECRET_KEY = ' ' #Secret KEY   这里可以自己去百度注册，这里是我的API KEY 和 Secret KEY

def bat(voice_path):
    token=""
    #设置音频的属性，采样率，格式等
    VOICE_RATE = 8000
    FILE_NAME = voice_path
    # USER_ID = '16241950' #这里的id随便填填就好啦，我填的自己昵称
    FILE_TYPE = 'wav'
    CUID="wate_play"   #用户唯一标识符，用来区分用户，可以修改
    #读取文件二进制内容
    f_obj = open(FILE_NAME, 'rb')
    content = base64.b64encode(f_obj.read())   # 百度语音识别需要base64编码格式
    speech = content.decode("utf-8")
    size = os.path.getsize(FILE_NAME)

    #json封装
    datas = json.dumps({      #json.dumps将一个Python数据结构转换为JSON ； json.loads将一个JSON编码的字符串转换回一个Python数据结构 
        'format': FILE_TYPE,
        'rate': VOICE_RATE,
        'channel': 1,
        'cuid': CUID,
        'token': token,   #上面从百度平台获取的token信息
        'speech': speech,
        'len': size,
        "dev_pid":"1537"
    })
    return datas

#设置headers和请求地址url
def post(datas):
    headers = {'Content-Type':'application/json'}
    #url = 'https://aip.baidubce.com/oauth/2.0/token?'  #技术文档中这个是获取token的url
    url = "http://vop.baidu.com/server_api"   #技术文档中给出的这个是语音识别的服务器接口

    #用post方法传数据
    request = requests.post(url, datas, headers)
    result = json.loads(request.text)
    # print('result:',result)
    text = result.get("result")
    if result['err_no'] == 0:
        return text
    else:
        return "Error"

#录音并将录音结果保存到filepath处in_path = C:\voice\voice.wav
def get_audio(filepath):
    try:
        input("回车开始录音 >>>")     #输出提示文本，input接收一个值,转为str，赋值给aa
    except KeyboardInterrupt:
        
        sys.exit()
    CHUNK = 256                 #定义数据流块(每个数据块儿存放位数，正好为一个字节)
    FORMAT = pyaudio.paInt16    #量化位数（音量级划分）
    CHANNELS = 1               # 声道数;声道数：可以是单声道或者是双声道
    RATE = 8000                # 采样率;采样率：一秒内对声音信号的采集次数，常用的有8kHz, 16kHz, 32kHz, 48kHz, 11.025kHz, 22.05kHz, 44.1kHz
    RECORD_SECONDS = 5          #录音秒数
    WAVE_OUTPUT_FILENAME = filepath     #wav文件路径
    p = pyaudio.PyAudio()               #实例化

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    print("*"*10, "开始录音:请在5秒内输入语音")
    frames = []                                                 #定义一个列表
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):      #循环，采样率(8000 / 256) * 5 = (8000*5) / 256
        data = stream.read(CHUNK)                               #读取chunk个字节 保存到data中
        frames.append(data)                                     #向列表frames中添加数据data
    # print(frames)
    print("*" * 10, "录音结束\n")

    stream.stop_stream()
    stream.close()          #关闭
    p.terminate()           #终结

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')                  #打开wav文件创建一个音频对象wf，开始写WAV文件
    wf.setnchannels(CHANNELS)                                   #配置声道数
    wf.setsampwidth(p.get_sample_size(FORMAT))                  #配置量化位数
    wf.setframerate(RATE)                                       #配置采样率
    wf.writeframes(b''.join(frames))                            #转换为二进制数据写入文件
    wf.close()              #关闭
    return

def check_disk():
    list_drive = psutil.disk_partitions()  # 找出本地磁盘列表，保存的是结构体对象
    list_disk = []
    for drive in list_drive:
        list_disk.append(drive.device)
    return list_disk

def recognition_text():

    dirname_path = os.path.join(os.getcwd(), "voice") # 设置语音文件存放路径
    
    if not os.path.exists(dirname_path):# 如果不存在该文件就创建一个该文件夹
        os.makedirs(dirname_path)

    filename = "voice.wav"  # 定义语音文件名
    in_path = os.path.join(dirname_path, filename)  
    # print('in_path:',in_path)   #录音文件保存在in_path
    get_audio(in_path) # 录音
    datas = bat(in_path) # 封装百度语音识别需要的配置信息，返回请求头
    res = post(datas) # 连接百度语音识别接口，得到识别结果
    #print("识别结果：",res)
    print(f"您输入的是：{res[0]}",)
    text=res[0].split("。")[0]
    return text