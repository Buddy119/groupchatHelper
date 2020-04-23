# coding=utf8
import itchat
from apscheduler.schedulers.background import BackgroundScheduler
import re
import time


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def text_reply(msg):
    global graph
    #print('start receive message')
    #print(msg['User']['NickName'])
    if msg['User']['NickName'] == chatroom:
        nameList = re.findall('(?<=@)[^\s]+\s?', msg.text)
        if(len(nameList) != 0):
            for name in nameList:
                print('This information is from ' + msg['ActualNickName'] + 'and send to ' + name)
                print('The msg is ' + msg.text)
                graph[name.strip()][msg['ActualNickName']].append(msg.text)
            view_graph()


def send(username, msg):
    user_info = itchat.search_friends(name=username)
    if len(user_info) > 0:
        user_name = user_info[0]['UserName']
        itchat.send_msg(msg, toUserName=user_name)


def send_msg():
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ' start send message')
    msg = ''
    #view_graph()
    for person in graph:
        for item in graph[person]:
            if len(graph[person][item]) != 0:
                msg += 'Below information is from ' + item + '\r\n'
                for line in graph[person][item]:
                    msg += line + ' \r\n'
                send(person, msg)
                msg = ''


def after_login():
    #print("after login")
    #sched.add_job(send_msg, 'cron', day_of_week ='0-6', hour=8, minute=0)
    #sched.add_job(clear_cache, 'cron', day_of_week ='0-6', hour=0, minute=5)
    sched.add_job(send_msg, 'interval', hours=1)
    sched.add_job(clear_cache, 'interval', hours =1, minutes=5)
    sched.start()


def clear_cache():
    for person in graph:
        for item in graph[person].values():
            if len(item) != 0:
                item.clear()


def after_logout():
    sched.shutdown()


def view_graph():
    for person in graph:
        for item in graph[person].values():
            if len(item) != 0:
                for line in item:
                    print(line)

def logout_callback():
    #print('Logout')
    itchat.auto_login(hotReload=True, exitCallback=logout_callback)


graph = {}

chatroom = ""
sched = BackgroundScheduler()
itchat.auto_login(hotReload=False, enableCmdQR=2, exitCallback=logout_callback)
after_login()
itchat.run()

