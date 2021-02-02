# -*- coding: utf-8 -*-
# !/usr/bin/env python
"""
-------------------------------------------------
   File     : TG Bot
   Author   : 红鲤鱼与绿鲤鱼与驴
   date     : 2021-2-1 9:32 
   Desc     : 公众号iosrule,编程测试与学习
   Gamerule: Tg群，微信学习，请勿用于非法用途
-------------------------------------------------
"""

import requests
import json
import time
import timeit
import os
import re
import urllib
from datetime import datetime
from dateutil import tz


tg_bot_id=''
tg_member_id=''
osenviron={}
telelist=[]
result=''
msglist=[]
idlist=[]
uslist=[]



SGlist=[]
NSlist=[]
MClist=[]
IDlist=[]

def bot_loadfile():
   global SGlist,NSlist,MClist,IDlist
   try:
      SGlist =bot_rd('SG.json','SG')
      MClist=bot_rd('MC.json','MC')
      NSlist=bot_rd('NS.json','NS')
      IDlist=bot_rd('ID.json','ID')
   except Exception as e:
      msg=str(e)
      print('bot_loadfile'+msg)
def bot_loadmsg():
   try:
      global msglist
      username=''
      msgtext=''
      msglist=[]
      res=requests.get(tg_bot_id,timeout=2000).json()
      if len(res['result'])==0:
        print('退出')
        return 
      i=0
      for data in res['result']:
        i+=1
        if 'username' in data['message']['chat']:
          username=data['message']['chat']['username']
        else:
          username='XX'
        id=data['message']['chat']['id']
        if 'text' in data['message']:
          msgtext=data['message']['text']
        else:
          msgtext='no msg'
        smslist=[]
        cc=False
        for i in range(len(msglist)):
          if id in msglist[i]:
             msglist[i].append(msgtext)
             msglist[i].append(data['message']['date'])
             cc=True
        if cc==False:
          smslist.append(id)
          smslist.append(username)
          smslist.append(msgtext)
          smslist.append(data['message']['date'])
          msglist.append(smslist)
          
          
        msgdate=datetime.fromtimestamp(data['message']['date']).strftime('%Y-%m-%d %H:%M:%S')
        #print('【'+str(i)+'】'+username+'_'+str(id)+'_'+msgtext+'_'+msgdate)
      print('圈友人数:'+str(len(msglist)))
      #print(msglist)
   except Exception as e:
      msg=str(e)
      print('loadbotmsg'+msg)
def bot_sendmsg(id,title,txt):
   try:
      txt=urllib.parse.quote(txt)
      title=urllib.parse.quote(title)
      turl=f'''{tg_member_id}chat_id={id}&text={title}\n{txt}'''
      response = requests.get(turl)
      #print(response.text)
   except Exception as e:
      msg=str(e)
      print(id+'_bot_sendmsg_'+msg)
def bot_chat(title,ckmsg,postmsg):
   try:
       print('bot_chat_'+title+'循环次数:',str(len(msglist)))
       if len(msglist)==0:
         return
       for i in range(len(msglist)):
          txttm=0
          checktm=0
          for j in range(len(msglist[i])):
            if msglist[i][j]==ckmsg:
               txttm=msglist[i][j+1]
          print('TG时间:'+str(txttm)+'-'+datetime.fromtimestamp(txttm).strftime('%Y-%m-%d %H:%M:%S')+'\n')
          checktm=tm10()-txttm
          print('bot第'+str(i)+'次运行中:',str(checktm),str(txttm))
          if checktm<60:
             print('机器人开始回复'+ckmsg)
             id=msglist[i][0]
             bot_sendmsg(id,title,postmsg)
             time.sleep(2)
   except Exception as e:
      msg=str(e)
      print('bot_chat:'+msg)
      
def bot_check():
   try:
      msg=['/help','提交码']
      menu=['1.活动字母简写,水果(SG),年兽(NS)\n2.SGxxxxxxxxx@yyyyyyyyy@zzzzzzz\nNSzzzzzzzzz@ggggggggggghgh\n3.不同活动互助码用换行开始,格式不对机器人不提交\n4.码提交后30-80秒后机器人确认回复.\n5.使用方法关注tg私人群邀请进去','您的JD互助码已经提交====']
      bot_chat('帮助功能:',msg[0],menu[0])
      bot_sub('提交功能:',msg[1],menu[1])
   except Exception as e:
      msg=str(e)
      print('bot_check:'+msg)

def bot_sub(title,ckmsg,postmsg):
   try:
     global SGlist,NSlist,MClist,IDlist
     num=0
     print('bot_sub_'+title+'循环次数:',str(len(msglist)))
     if len(msglist)==0:
         return
     for i in range(len(msglist)):
          txttm=0
          checktm=0
          for j in range(len(msglist[i])):
            if str(msglist[i][j]).find(ckmsg)>=0:
               num=j
               txttm=msglist[i][j+1]
          checktm=tm10()-txttm
          print('bot第'+str(i)+'次运行中:',str(checktm),str(txttm))
          if checktm<60:
              if num>0:
               SGlist= msg_clean(msglist[i][num],'SG')
               MClist=msg_clean(msglist[i][num],'MC')
               NSlist=msg_clean(msglist[i][num],'NS')
               id=msglist[i][0]
               print('机器人开始回复'+str(id)+':::'+ckmsg)
               if id in IDlist:
                 bot_sendmsg(id,title,'您已经提交过了\n')
                 time.sleep(2)
                 continue
               else:
                  IDlist.append(id)
                  bot_sendmsg(id,title,postmsg+'后台更新需要1个小时左右\n')
                  time.sleep(2)
             
   except Exception as e:
      msg=str(e)
      print('bot_sub:'+msg)

def msg_clean(msg,ckmsg):
   try:
     xlist=[]
     msg=msg.strip()[3:len(msg)]
     if msg.find(ckmsg)>=0:
       s1=msg.strip().split('\n')
       for i in s1:
         if i.find(ckmsg)==0:
           i=i[2:len(i)]
           s2=i.split('@')
           for j in s2:
            if j in xlist:
               continue
            xlist.append(j)
     if len(xlist)>0:
       return xlist
   except Exception as e:
      msg=str(e)
      print('msg_clean'+msg)
def bot_back(hd,xlist):
   if len(xlist)>0:
        return hd+str(xlist)+'\n'




def bot_wr(filename,hdname,JDlist):
   try:
     JDjson={}
     JDjson['code']=200
     JDjson['data']=JDlist
     JDjson["2021"]="仅仅作为测试tg互助码思路,不做更新和解释,by红鲤鱼与绿鲤鱼与驴，2021.1.30"
     JDjson["Sort"]=hdname+"数据"
     JDjson['Update_Time']=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f", )
     if len(JDlist)>0:
        with open("./"+filename,"w") as f:
          json.dump(JDjson,f)
          print(hdname+"写入文件完成...个数:"+str(len(JDlist)))
     else:
        print(hdname+"数据获取为空，不写入...")
   except Exception as e:
      msg=str(e)
      print(msg)

def bot_rd(filename,hd):
   try:
     JDjson={}
     xlist=[]
     with open("./"+filename,"r",encoding='utf8') as f:
       JDjson=json.load(f)
       if JDjson['code']==200:
         xlist=JDjson['data']
         print('读取'+hd+'文件完成...个数:'+str(len(xlist)))
         return xlist
   except Exception as e:
      msg=str(e)
      print('bot_rd:'+msg)
   
def tm10():
   Localtime=datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S.%f", )
   timeArray = datetime.strptime(Localtime, "%Y-%m-%d %H:%M:%S.%f")
   timeStamp = int(time.mktime(timeArray.timetuple()))
   return timeStamp
   
def clock(func):
    def clocked(*args, **kwargs):
        t0 = timeit.default_timer()
        result = func(*args, **kwargs)
        elapsed = timeit.default_timer() - t0
        name = func.__name__
        arg_str = ', '.join(repr(arg) for arg in args)
        print('[🔔运行完毕用时%0.8fs] %s(%s) -> %r' % (elapsed, name, arg_str, result))
        return result
    return clocked
    

def loaddata():
   global tg_bot_id,tg_member_id
   if "tg_bot_id" in os.environ:
      tg_bot_id = os.environ["tg_bot_id"]
   if "tg_bot_id" in osenviron:
      tg_bot_id = osenviron["tg_bot_id"]
   if not tg_bot_id:
       print(f'''【通知参数】 is empty,DTask is over.''')
       exit()
   if 'tg_member_id' in os.environ:
      tg_member_id = os.environ["tg_member_id"]
   if "tg_member_id" in osenviron:
      tg_member_id = osenviron["tg_member_id"]
   if not tg_member_id:
       print(f'''【通知参数】 is empty,DTask is over.''')
       exit()
       
       
def bot_inter():
   for i in range(6):
    loaddata()
    bot_loadmsg()
    bot_check()
    print('【'+str(i+1)+'】次运行完毕=======')
    print('心跳包运行中.....稍等30秒')
    time.sleep(30)
   

def bot_print():
   print('程序退出中稍后🔔=======')
   bot_wr('ID.json','ID',IDlist)
   bot_wr('SG.json','SG',SGlist)
   bot_wr('NS.json','NS',NSlist)
   bot_wr('MC.json','MC',MClist)
   print('程序结束🔔=======')
@clock
def start():
   
   print('Localtime',datetime.now(tz=tz.gettz('Asia/Shanghai')).strftime("%Y-%m-%d %H:%M:%S", ))
   bot_loadfile()
   bot_inter()
   bot_print()
if __name__ == '__main__':
       start()