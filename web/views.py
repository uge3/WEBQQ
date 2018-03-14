
# Create your views here.
from web import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import  authenticate,login,logout
from utils.check_code import create_validate_code
from web.forms import ArticleForm ,uploaded_img_file,callForm
from django.contrib.sessions.backends.db import SessionStore
from django.views.decorators import cache
from io import BytesIO
from utils.xss import XSSFilter
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from web.forms import UserForm
import json
from django.core.exceptions import ValidationError
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth.hashers import make_password, check_password
import datetime

def jsonp(request):
    func = request.GET.get('callback')
    content = '%s(100000)' %(func,)
    return HttpResponse(content)

#json 对错误信息对象进行处理
class JsonCustomEncoder(json.JSONEncoder):
    def default(self,field):
        if isinstance(field,ValidationError):#如果是错误信息进行处理
            return {'code':field.code ,'messages':field.messages}
        else:
            return json.JSONEncoder.default(self,field)


#首页
def index(request):
    count=Session.objects.count()#所有数量 session 表
    articles = models.Article.objects.all()#取出所有的文章
    return render(request, 'index.html',locals())

#版块
def category(request,category_id):
    articles = models.Article.objects.filter(category_id =category_id)#版块的ID
    return render(request,'index.html',locals())

#文章详情
def article_detail(request,article_id):
    try:
        article_obj=models.Article.objects.get(id=article_id)#文章ID

        if request.method=="POST":
            msg={}
            form = callForm(request.POST)#表单验证
            if form.is_valid():#如果验证成功
                comment = form.cleaned_data.pop('content')#取出文章内容
                comment = XSSFilter().process(comment)#进行处理 调用单例模式
                reply=request.POST.get('reply')#取出回复的ID
                user_id=request.user.id#取出回复的ID
                form_data=form.cleaned_data #表单数据
                form_data['user_id']=request.user.userprofile.id #加入作者 外键用ID
                form_data['article_id']=article_id #加入文章ID
                form_data['comment']=comment #加入内容
                if reply:
                    form_data['parent_comment_id']=reply #加入@对象
                    comment_obj=models.Comment(**form_data)#加入数据库 返回数据内容
                    comment_obj.save()#保存
                else:
                    comment_obj=models.Comment(**form_data)#加入数据库 返回数据内容
                    comment_obj.save()#保存

            else:
                print(form.errors)
                msg['errors']=form.errors
        return render(request,'article.html',locals())
    except ObjectDoesNotExist as e:
        return render(request,'404.html',{'error_msg':'文章不存在!'})


#发贴
def new_article(request):
    msg={}
    category_list=models.Category.objects.all()#版块列表
    if request.method=='POST':
        form =ArticleForm(request.POST,request.FILES)#文本,图片
        if form.is_valid():
            print(form.cleaned_data)
            form_data=form.cleaned_data #表单数据
            form_data['author_id']=request.user.userprofile.id #加入作者 外键用ID

            new_img_path = uploaded_img_file(request,request.FILES['head_img']) #自定义上传路径
            form_data['head_img']=new_img_path #修改存到数据库的路径

            new_article_obj=models.Article(**form_data)#加入数据库 返回数据内容
            new_article_obj.save()#保存
            return render(request,'new_article.html',locals())#返回新建的文章数据
        else:
            print(form.errors)
            msg['errors']=form.errors
    return render(request,'new_article.html',locals())

#登陆
def account_login(request):
    if request.method=="GET":
        return render(request,'login.html')
    elif request.method=="POST":
        result={'status': False,'error':None,'message':None}
        _username=request.POST.get('username')
        _password=request.POST.get('password')
        if request.POST.get('check_code').upper()!=request.session.get('CheckCode').upper():
            result['message'] = '验证码错误或者过期'
            return HttpResponse(json.dumps(result))
        user =authenticate(username=_username,password=_password)#调用用户认证模块
        if user:
            login(request,user)#记录登陆
            #如果自动登陆勾选
            rmb=request.POST.get('rmb')#
            if rmb:
                #设置超时时间
                request.session.set_expiry(60 * 60 * 24 * 30)
            result['status'] = True
        else:
            result['message'] = '用户名或密码错误'

        return HttpResponse(json.dumps(result))



#验证码函数
def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()#创建内存空间
    img, code = create_validate_code()#调用验证码图片生成函数 返回图片 和 对应的验证码
    img.save(stream, 'PNG')#保存为PNG格式
    request.session['CheckCode'] = code#保存在session中
    return HttpResponse(stream.getvalue())

#退出
def account_logout(request):
    logout(request)
    return HttpResponseRedirect('/')#跳转到首页


#注册
def register(request):
    '''
    '''
    if request.method=='GET':
        obj=UserForm(request.POST)
        return render(request, 'register.html',{'obj':obj})
    #context = {}
    elif request.method == 'POST':
        ret={'status':False,'error':None,'data':None}
        form = UserForm(request.POST)
        if form.is_valid():
            #获得表单数据
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email=form.cleaned_data['email']

            # 判断用户是否存在
            user = auth.authenticate(username = username,password = password)

            if not user:
                #添加到数据库（还可以加一些字段的处理）
                user = User.objects.create_user(username=username,email=email, password=password)
                user.save()
                usernames=models.UserProfile.objects.create(user_id=user.id,name=username)
                usernames.save()
            #添加到session
                request.session['username'] = usernames.name
                #调用auth登录
                login(request, user)
                ret['status']=True
                ret['data']=form.cleaned_data
                ret=json.dumps(ret,cls=JsonCustomEncoder)
            else:
                ret['error']={'user':'用户名重复'}
                ret=json.dumps(ret,cls=JsonCustomEncoder)

        else:
            ret['error']=form.errors.as_data()
            ret=json.dumps(ret,cls=JsonCustomEncoder)

        return HttpResponse(ret)
