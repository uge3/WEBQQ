from django.shortcuts import render,HttpResponse
from web_chat import models
import json,time
from queue import Queue
# Create your views here.
#全局消息队列
GLOBAL_MSG_Q={

}

#web聊天页面
def board(request):
    return render(request,'web_chat/board.html',locals())


#好友列表页面
def contacts(request):
    contact_dic={
        'contact_list':[],
        'group_list':[],
    }
    contacts_list=request.user.userprofile.friends.select_related().values('id','name')#取出所的好友
    contact_dic['contact_list']=list(contacts_list)
    groups=request.user.userprofile.qqgroup_set.select_related().values('id','name','max_member_nums')#群组
    contact_dic['group_list']=list(groups)
    return HttpResponse(json.dumps(contact_dic))


#发送消息
def msg(request):
    #print(request.POST.get('data'))
    if request.method=="GET":
        ''''''
        user_id =str(request.user.userprofile.id)#自己的id
        #print(user)
        msg_lists =[]
        if user_id in GLOBAL_MSG_Q:#如果有自己的消息
            msg_nums=GLOBAL_MSG_Q[user_id].qsize()#在队列的消息数量
            if msg_nums ==0:#没有新消息
                new_msg=GLOBAL_MSG_Q[user_id].get()
                print('进入阻塞时间')
                # msg_lists.append(GLOBAL_MSG_Q[user_id].get())#进入阻塞超时时间
                msg_lists.append(new_msg)
                print('超时时间')
            for i in range(msg_nums):#循环添加消息
                msg_lists.append(GLOBAL_MSG_Q[user_id].get())#队列中信息
            return HttpResponse(json.dumps(msg_lists))
        else:
            GLOBAL_MSG_Q[user_id]=Queue()
        return HttpResponse(json.dumps(msg_lists))
    elif request.method=="POST":
        try:
            data =json.loads(request.POST.get('data'))
            send_to=data['to']
            if send_to not in GLOBAL_MSG_Q:#如果没消息队列进行新建
                GLOBAL_MSG_Q[send_to]=Queue()
            data['times']=time.time()#加上时间
            GLOBAL_MSG_Q[send_to].put(data)#出队
            return HttpResponse(GLOBAL_MSG_Q[send_to].qsize())#消息
        except Exception as e:
            error='不存在'
            return HttpResponse(json.dumps(error))