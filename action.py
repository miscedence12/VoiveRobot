from geometry_msgs.msg import Twist
import rospy
import time
import subprocess
import re
import os
from Robot_voice.main import isExit
rospy.init_node("robot_byvoice",anonymous=True)#初始化结点
pub=rospy.Publisher("/cmd_vel",Twist,queue_size=10)#创建一个发布者，向话题发布消息
rate=rospy.Rate(10)#10HZ
vel_msg=Twist() #创建一个Twist类型的消息

def car_move_staright(linear=0,angular=0,target_time=None,text=None):
    global isExit
    if linear>=3 :
        linear=0.1*linear
    if angular>=2:
        angular=0.1*angular
    if target_time:
        rospy.loginfo(f"小车以{linear}m/s线速度{angular}rad/s角速度行驶{target_time}s{text}")
        if text=="前进":
            vel_msg.linear.x=linear
            vel_msg.angular.z=0
        elif text=="后退":
            vel_msg.linear.x=-linear
            vel_msg.angular.z=0
        elif text=="左转":
            vel_msg.linear.x=linear
            vel_msg.angular.z=angular
        elif text=="右转":
            vel_msg.linear.x=linear
            vel_msg.angular.z=-angular
        elif text==None:
            vel_msg.linear.x=linear
            vel_msg.angular.z=angular
        start_time=time.time()
        try:
            while not isExit:
                pub.publish(vel_msg)
                rate.sleep()
                current_time=time.time()
                if current_time-start_time>=int(target_time):
                    break
        except SystemExit:
            isExit=True
    else:
        rospy.loginfo(f"小车以{linear}m/s线速度{angular}rad/s角速度持续行驶") 
        if text=="前进":
            vel_msg.linear.x=linear
            vel_msg.angular.z=0
        elif text=="后退":
            vel_msg.linear.x=-linear
            vel_msg.angular.z=0
        elif text=="左转":
            vel_msg.linear.x=linear
            vel_msg.angular.z=angular
        elif text=="右转":
            vel_msg.linear.x=linear
            vel_msg.angular.z=-angular
        elif text==None:
            vel_msg.linear.x=linear
            vel_msg.angular.z=angular
        try:
            while not isExit:
                pub.publish(vel_msg)
                rate.sleep()
        except SystemExit:
            isExit=True
def find_value(text):
     # 使用正则表达式查找浮点数和整数  
    pattern = r"[-+]?\d*\.\d+|\d+|[一二三四五六七八九十零]"  
    matches = re.findall(pattern, text)  
    float_list=[]
    chinese_list=["零","一","二","三","四","五","六","七","八","九","十"]
    # 提取浮点数和整数并保存到列表中  
    for match in matches:  
        try:  
            float_value = float(match)  
            float_list.append(float_value)
        except ValueError:  
            if match in chinese_list:
                index=chinese_list.index(match)
                float_list.append(float(index))
    return float_list
def server_start():
    subprocess.call(["sh", "/home/jie/ui_server/server/server.sh"])
def server_close():
    os.chdir(os.getcwd())
    subprocess.call(["sh", "/home/jie/ui_server/server/server_close.sh"])
def ui_start():
    # os.chdir("/home/jie/ui_server/ui/")
    subprocess.call(["sh", "bash/ui.sh"])
def ui_stop():
    subprocess.call(["sh", "bash/ui_stop.sh"])


if __name__=="__main__":
    car_move_staright(0.1,target_time=2.0,text="前进")
    # ui_start()





    
    

