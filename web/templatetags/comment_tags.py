#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#BBS_web_QQ 
#2017/12/30    13:41
#__author__='Administrator'
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from utils.comment_tree import search_tree

register=template.Library()#注册为模板

def tree_search(data_dic,comment):#传入字典，上级，下级
    for k,v in data_dic.items():
        if comment.parent_comment==k: #如果等 于，找到上级
            data_dic[k][comment]={}#加到当前
            return
        else:
            tree_search(data_dic[k],comment)#传入下一层字典，上级，下级

#递归下级评论
def generate_comment(sub_comment,margin_left):
    html=""
    for k,v in sub_comment.items():
        html+="<div style='margin-left:%spx' class='comment-node reply'>"%margin_left+\
              "﹄@<span>"+k.parent_comment.user.name+"</span><span class='hide pid'>"+str(k.id)+"</span><br>&nbsp&nbsp&nbsp&nbsp<a class='calls'>"+k.user.name+"</a>:"+k.comment+"</div>"
        if v:
            html+=generate_comment(v,margin_left+15)#递归拼接
    return html

#评论
@register.simple_tag
def build_comment_tree(comment_list):
    #print(comment_list,'评论')
    for i in comment_list:
        print(i.id)
        print(i.user)
        print(i.parent_comment)
    '''
    data_dic={}  #转这的字典
    for comment in comment_list:

        if comment.parent_comment is None:#表示为顶级
            data_dic[comment]={}#如果为顶级，下级为KEY加入
        else: #如果不是顶级，查找上级
            tree_search(data_dic,comment)#调用查找

    '''
    data_dic={}#定义的字典
    comments=search_tree()#调用类，评论查找
    print(type(comments))
    comment_lists=comments.data_list(comment_list,data_dic)#传入评论表和字典
    print(type(comment_lists))

    #html拼接
    margin_left =0
    html="<div class='comment-box'>"
    for k,v in comment_lists.items():
        print(k.user.name,'.....')
        html+="<div class='reply'>评论人:<span class='hide pid'>"+str(k.id)+"</span><a class='calls'>"+k.user.name+"</a></div>"
        html+="<div style='margin-left:%spx'class='comment-node'>"%margin_left+"内容:"+k.comment+"</div>"
        html+=generate_comment(v,margin_left+15)#子级拼接
    html+="</div>"
    return mark_safe(html)