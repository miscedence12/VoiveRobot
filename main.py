import requests
import json
from edge import edge_tt
from baidu_voice_input import recognition_text
from playsound import playsound
import os
import asyncio
from datetime import datetime
from action import *
import signal
from threading import Thread

# engine = pyttsx3.init()
# import pyttsx3
# from VoiceInput import voice_input
#定义全局变量
isExit=False

#修改成自己的api key和secret key
API_KEY = ""
SECRET_KEY = ""
def main():
    global isExit
    token="可以运行get_access_token()获取token"
    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/eb-instant?access_token="+token
    while not isExit:
        # rospy.loginfo("请问有什么可以帮您的?")
        input_speak_path=os.path.join(current_path,"input.mp3")
        # # input_speak_path = input_speak_path.replace(" ", "%20")
        playsound(input_speak_path)
        s=recognition_text()
        try:
            yes=input("是否执行？(y or n)")
        except SystemExit:
            isExit=True
        # print(yes)
        if yes=="y":
            if s=='退出':
                output_speak_path=os.path.join(current_path,"output.mp3")
                # output_speak_path = output_speak_path.replace(" ", "%20")
                playsound(output_speak_path)
                isExit=True
                break
            elif s=="启动服务器":
                playsound(os.path.join(current_path,"voice","server_start.mp3"))
                server_start()
            elif s=="关闭服务器":
                playsound(os.path.join(current_path,"voice","server_stop.mp3"))
                server_close()
            elif s=="启动界面":
                playsound(os.path.join(current_path,"voice","ui_start.mp3"))
                ui_start()
            elif s=="关闭界面":
                playsound(os.path.join(current_path,"voice","ui_stop.mp3"))
                ui_stop()
            elif "线速度" in s or "角速度" in s or "秒" in s:
                l=["前进","后退","左转","右转"]
                for i in l:
                    if i in s:
                        text=i
                    else:
                        text=None 
                value_list=find_value(s)
                print(value_list)
                length=len(value_list)
                
                if "线速度" in s and length==1:
                    t1=Thread(target=car_move_staright,args=(value_list[0],0,None,text))
                    t1.start()
                elif "线速度" in s and "角速度" in s and length==2:
                    t2=Thread(target=car_move_staright,args=(value_list[0],value_list[1],None,text))
                    t2.start()
                elif "线速度" in s and "角速度" not in s and length==2:
                    t3=Thread(target=car_move_staright,args=(value_list[0],0,value_list[-1],text))
                    t3.start()
                elif length==3:
                    t4=Thread(target=car_move_staright,args=(value_list[0],value_list[1],value_list[-1],text))
                    t4.start()
            # s=voice_input()
            else:
            # 注意message必须是奇数条
                payload = json.dumps({
                "messages": [
                    {
                        "role": "user",
                        "content":"你现在的身份是机器人语音助手小文，你需要回答的问题是：" +s
                    }
                ]
                })
                headers = {
                    'Content-Type': 'application/json'
                }
                
                res = requests.request("POST", url, headers=headers, data=payload).json()
                # if res['error_code']==17:
                #     print( res['error_msg'])
                # else:
                text_response=res['result']
                print("小文：",text_response)
                asyncio.run(edge_tt(TEXT=text_response))
                response_speak_path=os.path.join(current_path,"response.mp3")
                # response_speak_path = response_speak_path.replace(" ", "%20")
                while not os.path.exists(response_speak_path):
                    continue

                playsound(response_speak_path)
        elif yes=="n":
            print("取消执行")
        else:
            print("请输入y or n")
 
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    print(requests.post(url, params=params).json().get("access_token"))
    return str(requests.post(url, params=params).json().get("access_token"))
def Exit(signum, data):
    global isExit
    isExit = True
    print("exit successfully")
    raise SystemExit(0)  # 抛出 SystemExit 异常

signal.signal(signal.SIGINT, Exit)

if __name__ == '__main__':
    # get_access_token()
    current_path = os.path.abspath(os.path.dirname(__file__))
    rospy.loginfo(f"当前目录为：{current_path}")
    current_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    current_date=current_time.split(" ")[0].replace("-","")
    # playsound(os.path.join(current_path,"password.mp3"))
    try:
        while not isExit:
            zhanghao=input("请输入您的账号：")
            password=input("请输入您的密码：")
            if zhanghao==current_date and password=="123456":
                rospy.loginfo("登录成功")
                rospy.loginfo("您好,我是您的机器人语音助手小文，您可以直接和我对话哦。")
                # playsound(os.path.join(current_path,"voice","introduce.mp3"))
                main()
                break
            else:
                rospy.loginfo("账号或密码错误，请您重新输入")
                playsound(os.path.join(current_path,"password2.mp3"))
    except SystemExit as e:
        isExit=True
    
 

