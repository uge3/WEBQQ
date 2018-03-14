#!usr/bin/env python
#-*-coding:utf-8-*-
# Author calmyan 
#BBS_web_QQ 
#2017/12/30    13:17
#__author__='Administrator'

#评论树
# data=[
#     (None,'a'),
#     ('a','a1'),
#     ('a1','a2'),
#     ('a','a1-2'),
# ]
#
# def tree_search(data_dic,parent,son):#传入字典，上级，下级
#     for k,v in data_dic.items():
#         if parent==k: #如果等 于，找到上级
#             data_dic[k][son]={}#加到当前
#            # print(data_dic)
#         else:
#             tree_search(data_dic[k],parent,son)#传入下一层字典，上级，下级
#
#
#
# data_dic={}  #转这的字典
# for item in data:
#     parent,son =item #评论上，下级
#     if parent is None:#表示为顶级
#         data_dic[son]={}#如果为顶级，下级为KEY加入
#     else: #如果不是顶级，查找上级
#         tree_search(data_dic,parent,son)#调用查找

# for k,v in data_dic.items():
#     print(k,v)

class search_tree(object):

    def tree_search(self,data_dic,comment):#传入字典，上级，下级
        for k,v in data_dic.items():
            if comment.parent_comment==k: #如果等 于，找到上级
                data_dic[k][comment]={}#加到当前
                return
            else:
                self.tree_search(data_dic[k],comment)#传入下一层字典，上级，下级

    def data_list(self,data,data_dic):
        #print(self.data,'data')
        for item in data:
             #评论上，下级
            if item.parent_comment is None:#表示为顶级
                data_dic[item]={}#如果为顶级，下级为KEY加入
            else: #如果不是顶级，查找上级
                self.tree_search(data_dic,item)#调用查找
        return data_dic


