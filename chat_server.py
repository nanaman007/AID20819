"""
chat from
env:python3.8
socket udp&fork
"""

from socket import  *
import  os,sys
"""
全局变量：很多封装模块都要用或者由一定的固定含义
"""
#服务器地址
ADDR = ('0.0.0.0',8888)
user={}

#登录
def do_login(s,name,addr):
    if name in user:
        s.sendto('该用户存在'.encode(),addr)
        return
    s.sendto(b'OK',addr)
    #通知其他人
    msg = "欢迎'%s'进入聊天室"%name
    for i in user:
        s.sendto(msg.encode(),user[i])
    user[name] = addr

#聊天
def do_chat(s,name,text):
    msg = "%s: %s"%(name,text)
    for i in user:
        if i is not name:
            s.sendto(msg.encode(),ADDR)

# 处理请求函数
def do_request(s):
    while True:
        data,addr = s.recvfrom(1024)
        tmp = data.decode().split(' ')#拆分请求
        #根据不同的请求类型具体执行不同的事情
        #L进入 C聊天  Q退出
        if tmp[0] == 'L':
            do_login(s,data,addr)  #执行具体工作
        elif tmp[0]=='C':
            text = ' '.join(tmp[2:])
            do_chat(s,tmp[1],text)

#搭建网络
def main():
    #udp服务端
    s = socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)
    do_request(s)

main()